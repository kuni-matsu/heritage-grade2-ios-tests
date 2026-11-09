import XCTest
import StoreKit
import StoreKitTest

final class SyntheticStoreKitTests: XCTestCase {
    @MainActor
    func testProductLookupPurchaseAndEntitlement() async throws {
        // Only synthetic StoreKit data is used; the paid question bank is not in this repository.
        let catalog = try XCTUnwrap(Bundle.main.url(forResource: "StoreKitSandbox", withExtension: "storekit"))
        // StoreKit's local test session must use the host application's catalog.
        let session = try SKTestSession(contentsOf: catalog)
        session.disableDialogs = true
        session.clearTransactions()

        let id = "jp.heritagemaster.grade2.fullaccess"
        let products = try await Product.products(for: [id])
        guard products.count == 1, let product = products.first else {
            XCTFail("Expected exactly one synthetic StoreKit product; received \(products.count)")
            return
        }
        XCTAssertEqual(product.id, id)
        XCTAssertEqual(product.type, .nonConsumable)
        XCTAssertEqual(product.price, Decimal(700))

        let outcome = try await product.purchase()
        guard case .success(let verification) = outcome,
              case .verified(let transaction) = verification else {
            XCTFail("Synthetic purchase did not return a verified transaction")
            return
        }
        XCTAssertEqual(transaction.productID, id)
        XCTAssertNil(transaction.revocationDate)
        await transaction.finish()

        // Re-reading StoreKit entitlements models a subsequent app launch. It does
        // not claim to test a full App Store sandbox sign-in or AppStore.sync().
        var hasAccess = false
        for await result in Transaction.currentEntitlements {
            if case .verified(let granted) = result,
               granted.productID == id,
               granted.revocationDate == nil {
                hasAccess = true
                break
            }
        }
        XCTAssertTrue(hasAccess, "Non-consumable entitlement should survive a fresh entitlement read")
        guard hasAccess else { return }

        // A refund must remove the paid entitlement. StoreKit propagates the
        // revocation asynchronously, so poll within a bounded 10-second window.
        guard let purchased = session.allTransactions().last(where: { $0.productIdentifier == id }) else {
            XCTFail("Purchased transaction is missing from the local StoreKit session")
            return
        }
        try session.refundTransaction(identifier: purchased.identifier)

        var accessAfterRefund = true
        for _ in 0..<50 {
            accessAfterRefund = false
            for await result in Transaction.currentEntitlements {
                if case .verified(let granted) = result,
                   granted.productID == id,
                   granted.revocationDate == nil {
                    accessAfterRefund = true
                    break
                }
            }
            if !accessAfterRefund { break }
            try await Task.sleep(nanoseconds: 200_000_000)
        }
        XCTAssertFalse(accessAfterRefund, "A refunded product must no longer grant paid access")
        guard !accessAfterRefund else { return }

        // Buying the same non-consumable again after a refund should restore
        // access using a NEW verified transaction, not a revoked purchase.
        let repurchase = try await product.purchase()
        guard case .success(let repurchaseResult) = repurchase,
              case .verified(let newTransaction) = repurchaseResult else {
            XCTFail("Refunded non-consumable could not be purchased again")
            return
        }
        XCTAssertEqual(newTransaction.productID, id)
        XCTAssertNil(newTransaction.revocationDate)
        XCTAssertNotEqual(newTransaction.id, transaction.id,
                          "Repurchase should create a different transaction")
        await newTransaction.finish()

        var accessRestored = false
        for _ in 0..<50 {
            for await result in Transaction.currentEntitlements {
                if case .verified(let granted) = result,
                   granted.productID == id, granted.revocationDate == nil {
                    accessRestored = true
                    break
                }
            }
            if accessRestored { break }
            try await Task.sleep(nanoseconds: 200_000_000)
        }
        XCTAssertTrue(accessRestored, "Buying again after a refund must restore paid access")
    }
}
