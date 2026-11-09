import Foundation
import StoreKit

public enum Grade2PurchaseCore {
    public static let productID = "jp.heritagemaster.grade2.fullaccess"

    public static func lookupProduct() async throws -> Product? {
        let products = try await Product.products(for: [productID])
        return products.first { $0.id == productID && $0.type == .nonConsumable }
    }

    public static func hasEntitlement() async -> Bool {
        for await result in Transaction.currentEntitlements {
            if case .verified(let transaction) = result,
               transaction.productID == productID,
               transaction.revocationDate == nil {
                return true
            }
        }
        return false
    }
}
