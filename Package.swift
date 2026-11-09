// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "Grade2StoreKitSandbox",
    platforms: [.iOS(.v16), .macOS(.v12)],
    products: [.library(name: "Grade2PurchaseCore", targets: ["Grade2PurchaseCore"])],
    targets: [
        .target(name: "Grade2PurchaseCore"),
        .testTarget(name: "Grade2PurchaseCoreTests", dependencies: ["Grade2PurchaseCore"])
    ]
)
