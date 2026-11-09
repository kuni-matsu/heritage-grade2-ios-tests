import XCTest
import StoreKit
import StoreKitTest
@testable import Grade2PurchaseCore

final class PurchaseCoreTests: XCTestCase {
    func testProductIDContract() {
        XCTAssertEqual(Grade2PurchaseCore.productID, "jp.heritagemaster.grade2.fullaccess")
    }

    #if os(iOS)
    @MainActor
    func testLocalStoreKitCatalogLoadsOnSimulator() async throws {
        guard let catalogURL = Bundle.module.url(forResource: "StoreKitSandbox", withExtension: "storekit") else {
            XCTFail("Bundled synthetic StoreKit catalog is missing")
            return
        }
        let session = try SKTestSession(contentsOf: catalogURL)
        session.disableDialogs = true
        session.clearTransactions()
        let product = try await Grade2PurchaseCore.lookupProduct()
        XCTAssertNotNil(product, "StoreKit returned no product from the synthetic local catalog")
        XCTAssertEqual(product?.id, Grade2PurchaseCore.productID)
        XCTAssertEqual(product?.type, .nonConsumable)
    }
    #endif
}
