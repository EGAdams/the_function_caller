My App was rejected by Apple and I need your help fixing it.  Here is the reason why they rejected it.
# Reason For the rejection
```
Guideline 3.1.1 - Business - Payments - In-App Purchase

We found that your app offers in-app purchases that can be restored but still does not include a "Restore Purchases" feature to allow users to restore the previously purchased in-app purchases, as specified in the "Restoring Purchase Products" section of the In-App Purchase Programming Guide:


"Users restore transactions to maintain access to content they've already purchased. For example, when they upgrade to a new phone, they don't lose all of the items they purchased on the old phone. Include some mechanism in your app to let the user restore their purchases, such as a Restore Purchases button."


Next Steps


To restore previously purchased in-app purchase products, it would be appropriate to provide a "Restore" button and initiate the restore process when the "Restore" button is tapped by the user. Note that automatically restoring purchases on launch will not resolve this issue.
```

Here is the html page that summarizes in app purchases:
In App purchase summary
```html
<!DOCTYPE html>
<html>
<body>
<div data-v-60225a94="" data-v-5bf7a092="" class="primary-content"><div data-v-15d7e6ba="" data-v-60225a94="" class="content"><h2 data-v-642ac6d4="" id="overview"><a data-v-642ac6d4="" href="/documentation/storekit/in-app_purchase#overview" aria-current="page" class="header-anchor router-link-exact-active router-link-active" data-after-text="in page link">Overview</a></h2><p>With the <span class="inline-link">In-App Purchase</span> API, you can offer customers the opportunity to purchase digital content and services in your app. Customers can make the purchases within your app, and find your promoted products on the App Store. </p><p>The StoreKit framework connects to the App Store on your app's behalf to prompt for, and securely process, payments. The framework then notifies your app, making the transactions for In-App Purchases available to your app on all of the customer's devices. For each transaction that represents a current purchase, your app delivers the purchased products. To validate purchases, you can verify transactions on your server, or rely on StoreKit's verification. </p><p class="inline-image-container"><figure id="4447232"></figure></p><p>The App Store can also communicate with your server. It notifies your server of transactions and auto-renewable subscription events through <a href="/documentation/appstoreservernotifications" class="inline-link">App Store Server Notifications</a>, and provides the same transaction information, and more, through the <a href="/documentation/appstoreserverapi" class="inline-link">App Store Server API</a>.</p><p>To learn how adding In-App Purchases fits in an overall app development workflow for the App Store, see <a href="https://developer.apple.com/app-store/pathway/" class="inline-link">App Store Pathway</a>. For an overview of In-App Purchases and its features, including its configuration, testing capabilities, marketing for your products, and more, see <a href="https://developer.apple.com/in-app-purchase/" class="inline-link">Simple and safe In-App Purchases</a>. For an overview on subscriptions, including creating subscription groups, Family Sharing, and more, see <a href="https://developer.apple.com/app-store/subscriptions/" class="inline-link">Auto-renewable subscriptions</a>.</p><h3 data-v-642ac6d4="" id="3820031"><a data-v-642ac6d4="" href="/documentation/storekit/in-app_purchase#3820031" class="header-anchor" data-after-text="in page link">Configure In-App Purchases </a></h3><p>To use the <span class="inline-link">In-App Purchase</span> API, you first need to configure the products that your app merchandises. </p><ul><li><p>In the early stages of development, you can configure the products in the StoreKit configuration file in Xcode, and test your code without any dependency on App Store Connect. For more information, see <a href="/documentation/xcode/setting-up-storekit-testing-in-xcode" class="inline-link">Setting up StoreKit Testing in Xcode</a>.</p></li><li><p>When you're ready for sandbox testing and production, configure the products in App Store Connect. You can add or remove products and refine or reconfigure existing products as you develop your app. For more information, see <a href="https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases" class="inline-link">Configure In-App Purchase settings</a>.</p></li></ul><p>You can also offer apps and In-App Purchases that run on multiple platforms as a single purchase. For more information on universal purchase, see <a href="https://developer.apple.com/help/app-store-connect/create-an-app-record/add-platforms/" class="inline-link">Add platforms</a>.</p><h3 data-v-642ac6d4="" id="4446324"><a data-v-642ac6d4="" href="/documentation/storekit/in-app_purchase#4446324" class="header-anchor" data-after-text="in page link">Support a store in your app</a></h3><p>The <span class="inline-link">In-App Purchase</span> API takes advantage of Swift features like concurrency to simplify your In-App Purchase workflows, and SwiftUI to build stores with <a href="/documentation/storekit/in-app_purchase/storekit_views" class="inline-link">StoreKit views</a>. Use the API to manage access to content and subscriptions, receive App Store-signed transaction information, get the history of all In-App Purchase transactions, and more.</p><aside data-v-0ca053f3="" aria-label="note" class="note"><p data-v-0ca053f3="" class="label">Related sessions from WWDC21</p><p data-v-0ca053f3="">Session 10114: <a href="https://developer.apple.com/videos/play/wwdc2021/10114/" class="inline-link" data-v-0ca053f3="">Meet StoreKit 2</a></p></aside><p>The <span class="inline-link">In-App Purchase</span> API offers:</p><ul><li><p>Transaction information that's App Store-signed in JSON Web Signature (JWS) format.</p></li><li><p>Transaction and subscription status information that's simple to parse in your app.</p></li><li><p>An entitlements API, <a href="/documentation/storekit/transaction/3851204-currententitlements" class="inline-link"><code data-v-88c637be="">current<wbr data-v-88c637be="">Entitlements</code></a>, that simplifies determining entitlements to unlock content and services for your customers.</p></li></ul><aside data-v-0ca053f3="" aria-label="note" class="note"><p data-v-0ca053f3="" class="label">Related sessions from WWDC22</p><p data-v-0ca053f3="">Session 110404: <a href="https://developer.apple.com/videos/play/wwdc2022/110404/" class="inline-link" data-v-0ca053f3="">Implement proactive in-app purchase restore</a> </p></aside><p>To support a store in your app, implement the following functionality:</p><ul><li><p>Listen for transaction state changes using the transaction listener, <a href="/documentation/storekit/transaction/3851206-updates" class="inline-link"><code data-v-88c637be="">updates</code></a>, to provide up-to-date service and content while your app is running.</p></li><li><p>Use <span class="inline-link">StoreKit views</span> to merchandise your products; or request products to display from the App Store with <a href="/documentation/storekit/product/3851116-products" class="inline-link"><code data-v-88c637be="">products(for:)</code></a> and enable purchases using <a href="/documentation/storekit/product/3791971-purchase" class="inline-link"><code data-v-88c637be="">purchase(options:)</code></a>. Unlock purchased content and services based on the purchase result, <a href="/documentation/storekit/product/purchaseresult" class="inline-link"><code data-v-88c637be="">Product<wbr data-v-88c637be="">.Purchase<wbr data-v-88c637be="">Result</code></a>.</p></li><li><p>Iterate through a customer's purchases anytime using the transaction sequence <a href="/documentation/storekit/transaction/3851203-all" class="inline-link"><code data-v-88c637be="">all</code></a>, and unlock the purchased content and services.</p></li><li><p>Optionally, validate the signed transactions and signed subscription status information that you receive from the API.</p></li></ul></div></div>
</body>
</html>
```

Here is the Swift source code for the Subscription View Controller that got rejected.
# Source code for the existing subscription view controller
```swift
import UIKit
import StoreKit
import SafariServices

protocol SubscriptionViewControllerDelegate: AnyObject {
    func subscriptionViewControllerDidFailTransaction(_ controller: SubscriptionViewController, error: String)
}

class SubscriptionViewController: UIViewController {

    weak var delegate: SubscriptionViewControllerDelegate?
    private let subscribeButton = UIButton(type: .system)
    private let productDescriptionLabel = UILabel()
    private let priceLabel = UILabel()
    private let autoRenewalLabel = UILabel()
    private let renewalTermsLabel = UILabel()
    private let eulaButton = UIButton(type: .system)
    private let privacyPolicyButton = UIButton(type: .system)
    private let titleLabel = UILabel()
    private let containerView = UIView()
    private var subscriptionProducts: [SKProduct] = []
    private var selectedProduct: SKProduct?

    @objc private func privacyPolicyTapped() {
        guard let url = URL(string: "https://airportnac.com/privacy-policy/") else { return }
        let safariVC = SFSafariViewController(url: url)
        present(safariVC, animated: true, completion: nil)
    }

    init(subscriptionProducts: [SKProduct]) {
        self.subscriptionProducts = subscriptionProducts
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor.black.withAlphaComponent(0.5)
        setupViews()
        displayProductInfo()
    }

    @objc private func subscribeTapped() {
        guard let product = selectedProduct else { return }
        let payment = SKPayment(product: product)
        SKPaymentQueue.default().add(payment)
    }

    @objc private func eulaTapped() {
        guard let url = URL(string: "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/") else { return }
        let safariVC = SFSafariViewController(url: url)
        present(safariVC, animated: true, completion: nil)
    }

    private func displayProductInfo() {
        guard !subscriptionProducts.isEmpty else {
            productDescriptionLabel.text = "Subscription information unavailable."
            return
        }

        selectedProduct = subscriptionProducts.first
        updateProductDetails(for: selectedProduct)
    }

    private func updateProductDetails(for product: SKProduct?) {
        guard let product = product else { return }

        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.locale = product.priceLocale
        let priceString = formatter.string(from: product.price) ?? "N/A"

        if let subscriptionPeriod = product.subscriptionPeriod {
            let unit: String
            switch subscriptionPeriod.unit {
            case .day:
                unit = "day"
            case .week:
                unit = "week"
            case .month:
                unit = "month"
            case .year:
                unit = "year"
            @unknown default:
                unit = "period"
            }

            let periodString = "\(subscriptionPeriod.numberOfUnits) \(unit)\(subscriptionPeriod.numberOfUnits > 1 ? "s" : "")"

            // Update title label
            titleLabel.text = "\(product.localizedTitle) (\(periodString))"

            // Update product description label
            productDescriptionLabel.text = "Unlock all features with our \(periodString) subscription."

            // Update price label
            priceLabel.text = "Price: \(priceString)/\(unit)"

            // Update autoRenewalLabel
            autoRenewalLabel.text = "Auto-renews at \(priceString)/\(unit). Cancel anytime in Settings."
        } else {
            // If no subscription period, handle accordingly
            titleLabel.text = product.localizedTitle
            productDescriptionLabel.text = product.localizedDescription
            priceLabel.text = "Price: \(priceString)"
            autoRenewalLabel.text = "Auto-renews at \(priceString). Cancel anytime in Settings."
        }
    }

    private func setupViews() {
        // Configure container view
        containerView.backgroundColor = .white
        containerView.layer.cornerRadius = 20
        containerView.layer.borderColor = UIColor.lightGray.cgColor
        containerView.layer.borderWidth = 1.0
        containerView.layer.masksToBounds = true
        view.addSubview(containerView)

        containerView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            containerView.widthAnchor.constraint(equalTo: view.widthAnchor, multiplier: 0.8),
            containerView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            containerView.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])

        // Title Label
        titleLabel.textAlignment = .center
        titleLabel.font = UIFont.boldSystemFont(ofSize: 24)

        // Product Description
        productDescriptionLabel.textAlignment = .center
        productDescriptionLabel.font = UIFont.systemFont(ofSize: 18)
        productDescriptionLabel.numberOfLines = 0

        // Price Label
        priceLabel.textAlignment = .center
        priceLabel.font = UIFont.systemFont(ofSize: 18)

        // Auto-Renewal Notice
        autoRenewalLabel.textAlignment = .center
        autoRenewalLabel.font = UIFont.systemFont(ofSize: 14)
        autoRenewalLabel.textColor = .gray
        autoRenewalLabel.numberOfLines = 0

        // Renewal Terms Label
        renewalTermsLabel.text = "This subscription automatically renews unless canceled at least 24 hours before the end of the current period."
        renewalTermsLabel.textAlignment = .center
        renewalTermsLabel.font = UIFont.systemFont(ofSize: 14)
        renewalTermsLabel.textColor = .gray
        renewalTermsLabel.numberOfLines = 0

        // Privacy Policy Button
        privacyPolicyButton.setTitle("Privacy Policy", for: .normal)
        privacyPolicyButton.setTitleColor(.systemBlue, for: .normal)
        privacyPolicyButton.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        privacyPolicyButton.addTarget(self, action: #selector(privacyPolicyTapped), for: .touchUpInside)

        // EULA Button
        eulaButton.setTitle("View EULA", for: .normal)
        eulaButton.setTitleColor(.systemBlue, for: .normal)
        eulaButton.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        eulaButton.addTarget(self, action: #selector(eulaTapped), for: .touchUpInside)

        // Subscribe Button
        subscribeButton.setTitle("Subscribe", for: .normal)
        subscribeButton.setTitleColor(.white, for: .normal)
        subscribeButton.backgroundColor = .systemBlue
        subscribeButton.layer.cornerRadius = 10
        subscribeButton.titleLabel?.font = UIFont.boldSystemFont(ofSize: 18)
        subscribeButton.addTarget(self, action: #selector(subscribeTapped), for: .touchUpInside)

        // Configure buttons stack view
        let buttonsStackView = UIStackView()
        buttonsStackView.axis = .vertical
        buttonsStackView.alignment = .center
        buttonsStackView.distribution = .equalSpacing
        buttonsStackView.spacing = 10

        buttonsStackView.addArrangedSubview(privacyPolicyButton)
        buttonsStackView.addArrangedSubview(eulaButton)
        buttonsStackView.translatesAutoresizingMaskIntoConstraints = false

        // Add subviews
        containerView.addSubview(titleLabel)
        containerView.addSubview(productDescriptionLabel)
        containerView.addSubview(priceLabel)
        containerView.addSubview(autoRenewalLabel)
        containerView.addSubview(buttonsStackView)
        containerView.addSubview(subscribeButton)
        containerView.addSubview(renewalTermsLabel)

        // Constraints
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        productDescriptionLabel.translatesAutoresizingMaskIntoConstraints = false
        priceLabel.translatesAutoresizingMaskIntoConstraints = false
        autoRenewalLabel.translatesAutoresizingMaskIntoConstraints = false
        subscribeButton.translatesAutoresizingMaskIntoConstraints = false
        renewalTermsLabel.translatesAutoresizingMaskIntoConstraints = false

        NSLayoutConstraint.activate([
            titleLabel.topAnchor.constraint(equalTo: containerView.topAnchor, constant: 20),
            titleLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 20),
            titleLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -20),

            productDescriptionLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 10),
            productDescriptionLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 20),
            productDescriptionLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -20),

            priceLabel.topAnchor.constraint(equalTo: productDescriptionLabel.bottomAnchor, constant: 10),
            priceLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 20),
            priceLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -20),

            autoRenewalLabel.topAnchor.constraint(equalTo: priceLabel.bottomAnchor, constant: 10),
            autoRenewalLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 20),
            autoRenewalLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -20),

            buttonsStackView.topAnchor.constraint(equalTo: autoRenewalLabel.bottomAnchor, constant: 10),
            buttonsStackView.centerXAnchor.constraint(equalTo: containerView.centerXAnchor),

            subscribeButton.topAnchor.constraint(equalTo: buttonsStackView.bottomAnchor, constant: 20),
            subscribeButton.centerXAnchor.constraint(equalTo: containerView.centerXAnchor),
            subscribeButton.widthAnchor.constraint(equalToConstant: 150),
            subscribeButton.heightAnchor.constraint(equalToConstant: 40),

            renewalTermsLabel.topAnchor.constraint(equalTo: subscribeButton.bottomAnchor, constant: 10),
            renewalTermsLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor, constant: 20),
            renewalTermsLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor, constant: -20),
            renewalTermsLabel.bottomAnchor.constraint(equalTo: containerView.bottomAnchor, constant: -20)
        ])
    }
    
    func handleTransactionError(_ errorMessage: String) {
        // Display an alert to inform the user about the transaction error
        let alert = UIAlertController(title: "Transaction Error", message: errorMessage, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
        present(alert, animated: true, completion: nil)
    }
}
```
# Your Task
Please rewrite the SubscriptionViewController to conform to Apple's requirements.
