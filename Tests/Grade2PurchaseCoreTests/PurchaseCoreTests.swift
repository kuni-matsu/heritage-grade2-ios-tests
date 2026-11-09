import XCTest
@testable import Grade2PurchaseCore

final class PurchaseCoreTests: XCTestCase {
    func testProductIDContract() {
        XCTAssertEqual(Grade2PurchaseCore.productID, "jp.heritagemaster.grade2.fullaccess")
    }
}
