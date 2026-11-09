import XCTest
import StoreKit
import StoreKitTest

final class SyntheticStoreKitTests: XCTestCase {
    @MainActor
    func testProductLookupWithLocalStoreKitSession() async throws {
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: "StoreKitSandbox", withExtension: "storekit"))
        let session = try SKTestSession(contentsOf: url)
        session.disableDialogs = true
        session.clearTransactions()
        let id = "jp.heritagemaster.grade2.fullaccess"
        let products = try await Product.products(for: [id])
        XCTAssertEqual(products.count, 1, "The synthetic product must be visible in the hosted iOS test")
        XCTAssertEqual(products.first?.id, id)
        XCTAssertEqual(products.first?.type, .nonConsumable)
    }
}
