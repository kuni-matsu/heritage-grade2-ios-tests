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
    }
}
