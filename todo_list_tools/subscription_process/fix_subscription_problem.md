Here is the code to show the Subscription View:
```swift
import UIKit
import StoreKit
import SafariServices // Import SafariServices for SFSafariViewController

protocol SubscriptionViewControllerDelegate: AnyObject {
    func subscriptionViewControllerDidFailTransaction(_ controller: SubscriptionViewController, error: String)
}

class SubscriptionViewController: UIViewController {
    
    weak var delegate: SubscriptionViewControllerDelegate?
    private let subscribeButton = UIButton(type: .system)
    private let productDescriptionLabel = UILabel()
    private let priceLabel = UILabel()
    private let productIdentifierLabel = UILabel()
    private let eulaButton = UIButton(type: .system) // New UIButton for EULA
    private let titleLabel = UILabel()
    private var subscriptionProduct: SKProduct?

    init(subscriptionProduct: SKProduct?) {
        self.subscriptionProduct = subscriptionProduct
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = .white
        setupViews()
        displayProductInfo()
    }
    
    @objc private func subscribeTapped() {
        guard let product = subscriptionProduct else { return }
        let payment = SKPayment(product: product)
        SKPaymentQueue.default().add(payment)
    }
    
    @objc private func eulaTapped() {
        guard let url = URL(string: "https://airportnac.com/terms-and-conditions/") else { return }
        let safariVC = SFSafariViewController(url: url)
        present(safariVC, animated: true, completion: nil)
    }
    
    func handleTransactionError(_ error: String) {
        delegate?.subscriptionViewControllerDidFailTransaction(self, error: error)
    }
    
    private func setupViews() {
        // Set up title label
        titleLabel.text = "Subscribe to Unlock Features"
        titleLabel.textAlignment = .center
        titleLabel.font = UIFont.boldSystemFont(ofSize: 24)
        
        // Set up product description label
        productDescriptionLabel.textAlignment = .center
        productDescriptionLabel.font = UIFont.systemFont(ofSize: 18)
        productDescriptionLabel.numberOfLines = 0
        
        // Set up EULA button
        eulaButton.setTitle("View EULA", for: .normal)
        eulaButton.setTitleColor(.systemBlue, for: .normal)
        eulaButton.titleLabel?.font = UIFont.systemFont(ofSize: 16)
        eulaButton.addTarget(self, action: #selector(eulaTapped), for: .touchUpInside)
        
        // Set up price label
        priceLabel.textAlignment = .center
        priceLabel.font = UIFont.boldSystemFont(ofSize: 20)
        
        // Set up product identifier label
        productIdentifierLabel.textAlignment = .center
        productIdentifierLabel.font = UIFont.systemFont(ofSize: 14)
        productIdentifierLabel.textColor = .gray
        productIdentifierLabel.numberOfLines = 1
        
        // Set up subscribe button
        subscribeButton.setTitle("Subscribe", for: .normal)
        subscribeButton.setTitleColor(.white, for: .normal)
        subscribeButton.backgroundColor = .systemBlue
        subscribeButton.layer.cornerRadius = 10
        subscribeButton.layer.masksToBounds = true
        subscribeButton.titleLabel?.font = UIFont.boldSystemFont(ofSize: 18)
        subscribeButton.addTarget(self, action: #selector(subscribeTapped), for: .touchUpInside)
        
        // Add views
        view.addSubview(titleLabel)
        view.addSubview(productDescriptionLabel)
        view.addSubview(eulaButton) // Add EULA button to the view
        view.addSubview(priceLabel)
        view.addSubview(productIdentifierLabel)
        view.addSubview(subscribeButton)
        
        // Layout constraints
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        productDescriptionLabel.translatesAutoresizingMaskIntoConstraints = false
        eulaButton.translatesAutoresizingMaskIntoConstraints = false
        priceLabel.translatesAutoresizingMaskIntoConstraints = false
        productIdentifierLabel.translatesAutoresizingMaskIntoConstraints = false
        subscribeButton.translatesAutoresizingMaskIntoConstraints = false
        
        NSLayoutConstraint.activate([
            // Title Label Constraints
            titleLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 40),
            titleLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            titleLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            
            // Product Description Label Constraints
            productDescriptionLabel.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 20),
            productDescriptionLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            productDescriptionLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            
            // EULA Button Constraints
            eulaButton.topAnchor.constraint(equalTo: productDescriptionLabel.bottomAnchor, constant: 10),
            eulaButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            
            // Price Label Constraints
            priceLabel.topAnchor.constraint(equalTo: eulaButton.bottomAnchor, constant: 20),
            priceLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            
            // Product Identifier Label Constraints
            productIdentifierLabel.topAnchor.constraint(equalTo: priceLabel.bottomAnchor, constant: 8),
            productIdentifierLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            productIdentifierLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            
            // Subscribe Button Constraints
            subscribeButton.topAnchor.constraint(equalTo: productIdentifierLabel.bottomAnchor, constant: 30),
            subscribeButton.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            subscribeButton.widthAnchor.constraint(equalToConstant: 200),
            subscribeButton.heightAnchor.constraint(equalToConstant: 50)
        ])
    }
    
    private func displayProductInfo() {
        guard let product = subscriptionProduct else {
            productDescriptionLabel.text = "Subscription information unavailable."
            priceLabel.text = ""
            productIdentifierLabel.text = ""
            return
        }
        
        productDescriptionLabel.text = product.localizedDescription
        
        // Format the price using the locale of the user
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.locale = product.priceLocale
        let priceString = formatter.string(from: product.price) ?? "N/A"
        
        priceLabel.text = "Price: \(priceString) per year"
        productIdentifierLabel.text = "Product ID: \(product.productIdentifier)" // Set the product identifier text
    }
}
```

Here is the code for the ViewController that uses the SubscriptionViewController:
```swift
import UIKit
import StoreKit
class ViewController: UIViewController, SKProductsRequestDelegate, SKPaymentTransactionObserver, ReviewViewControllerDelegate {
    private let yearlySubscriptionProductID = "yearly_subscription_1234"
    private var yearlySubscriptionProduct: SKProduct?
    private var isSubscribed = false
    
    deinit { // Remove observer when ViewController is deallocated
        SKPaymentQueue.default().remove( self )}

    func didRequestDeleteProgram() {
        print ( "did request delete program called inside the ViewController..." )
        removeProgram()}
    
    
    
    @IBOutlet weak var start_button: UIButton!
    @IBOutlet weak var version_text: UITextView!
    @IBOutlet weak var new_button: UIButton!
    @IBOutlet weak var previousProgram: UIButton!
    @IBOutlet weak var nextProgram: UIButton!
    @IBOutlet weak var delete_button: UIButton!

    @IBOutlet weak var configure_button: UIButton!
    @IBOutlet weak var review_button: UIButton!
    var programs: [ Program ] = []
    let initial_blank_test_array: [ Test ] = []
    var current_program_index: Int = 0 {
        didSet {
            print ( "didSet called" )
            print ( "programs.count: \( String( describing: programs.count )) " )
            DispatchQueue.main.async {
                self.previousProgram.isEnabled   = self.programs.count > 0
                self.nextProgram.isEnabled       = self.programs.count > 0
                self.start_button.isEnabled      = self.programs.count > 0
                self.configure_button.isEnabled  = self.programs.count > 0
                self.review_button.isEnabled     = self.programs.count > 0
                self.delete_button.isEnabled     = self.programs.count > 0
                self.previousProgram.isEnabled   = self.programs.count > 0
                self.nextProgram.isEnabled       = self.programs.count > 0
                self.commentsTextView.text = "You do not have any programs.  Use the New button to create the program."
            }
        }}
    
    override func shouldPerformSegue(withIdentifier identifier: String, sender: Any?) -> Bool {
            if identifier == "speed_scale_vc_segue" {
                if !isSubscribed {
                    // Optionally, show an alert to inform the user about the subscription requirement
                    // let alert = UIAlertController(title: "Subscription Required", message: "You need to be subscribed to access this feature.", preferredStyle: .alert)
                    // alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                    // present(alert, animated: true, completion: nil)
                    
                    return false  // Cancel the segue
                }
            }
            return true  // Proceed with the segue if isSubscribed is true
        }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "add_program_vc_segue" {
            if let addProgramViewController = segue.destination as? AddProgramViewController {
                print( "setting ProgramCridVC to self..." )
                addProgramViewController.delegate = self
            }
        } else if segue.identifier == "speed_scale_vc_segue" { 
            if let speedScaleVC = segue.destination as? SpeedScaleViewController {
                print( "the current program index is: \(current_program_index)" )
                print( "switching and sending program id to the speed scale view controller..." )
                speedScaleVC.setCurrentProgramIndex(index: self.current_program_index )
            }
        } else if segue.identifier == "review_vc_segue" { 
            if let reviewViewController = segue.destination as? ReviewViewController {
                print( "the current program index is: \(current_program_index)" )
                print( "switching and sending program id to the review view controller..." )
                reviewViewController.setCurrentProgramIndex( index: self.current_program_index )
                reviewViewController.delegate = self
            }
        }
    }
    
  
    
    @IBAction func new_program(_ sender: Any) { print ( "new program pressed." )}
    var currentProgram: Program? = nil
    var accelerationController: AccelerationController?
    let programDataSource = ProgramDataSource()
    @IBOutlet weak var commentsTextView: UITextView!
    @IBAction func deleteProgram( _ sender: UIButton ) { print( "delete button pressed." ); removeProgram()}
    @IBAction func nextProgram( _ sender: Any) { nextButtonTapped()}
    @IBAction func previousProgram( _ sender: UIButton ) { previousButtonTapped()}
    
    @objc func previousButtonTapped() {
        print ( "previous button tapped. " )
        if current_program_index > 0 {
            current_program_index -= 1
            currentProgram = programs[ current_program_index ]
            updateUI()}}
    
    @objc func nextButtonTapped() {
        print ( "next button tapped. " )
        if current_program_index < programs.count - 1 {
            current_program_index += 1
            currentProgram = programs[ current_program_index ]
            updateUI()}}
    
    /*
     *  Since the centerTextViewVertically method itself is being called from within an asynchronous dispatch
     *  to the main thread, you do not need to wrap its contents again in DispatchQueue.main.async.  Just make
     *  sure that this method is never called from anywhere but the main thread.
     */
    func centerTextViewVertically(_ textView: UITextView) {         // wrapped in below method
        let textViewSize = textView.sizeThatFits(CGSize(width: textView.frame.size.width, height: CGFloat.infinity))
        let topBottomInsets = max((textView.bounds.size.height - textViewSize.height) / 2, 0)
        textView.contentInset = UIEdgeInsets(top: topBottomInsets, left: 0, bottom: topBottomInsets, right: 0)
    }
    
    /* 
       The viewDidLayoutSubviews method is called as part of the layout process, which occurs on the main thread.
       Therefore, wrapping UI updates in DispatchQueue.main.async within this method is generally unnecessary, as
       the method itself is guaranteed to be called on the main thread.
     */
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()                               // Call this first, synchronously
        if let commentsTextView = self.commentsTextView {           // Safely unwrap commentsTextView before using it
            commentsTextView.textAlignment = .left                  // Horizontally center
            self.centerTextViewVertically(commentsTextView)         // Vertically center
        }
    }

    func updateTextViewWithFormattedText(airportName: String, locationOfTest: String, comments: String) {
        let regularAttributes: [NSAttributedString.Key: Any] = [.font: UIFont.systemFont(ofSize: 16)]
        let boldAttributes: [NSAttributedString.Key: Any] = [.font: UIFont.boldSystemFont(ofSize: 16)]
        let formattedString = NSMutableAttributedString()
        let airportNameTitle = NSAttributedString(string: "Airport name\n", attributes: boldAttributes)          // Airport Name
        let airportNameValue = NSAttributedString(string: "\(airportName)\n\n", attributes: regularAttributes)
        formattedString.append(airportNameTitle)
        formattedString.append(airportNameValue)
        let locationTitle = NSAttributedString(string: "Location of Test\n", attributes: boldAttributes)        // Location of Test
        let locationValue = NSAttributedString(string: "\(locationOfTest)\n\n", attributes: regularAttributes)
        formattedString.append(locationTitle)
        formattedString.append(locationValue)
        let commentsTitle = NSAttributedString(string: "Comments\n", attributes: boldAttributes)
        let commentsValue = NSAttributedString(string: "\(comments)\n", attributes: regularAttributes)
        formattedString.append(commentsTitle)
        formattedString.append(commentsValue)
        DispatchQueue.main.async { [weak self] in  // Get off the main thread and set the formatted text to the UITextView
            self?.commentsTextView.attributedText = formattedString
            self?.commentsTextView.setNeedsDisplay()
            let top = CGPoint(x: 0, y: 0)
            self?.commentsTextView.setContentOffset(top, animated: false)
        }
    }
    
    private func fetchSubscriptionProduct() {        // Fetches the subscription product info from App Store
        print( "fetching subscription product..." )
        if SKPaymentQueue.canMakePayments() {
            let productRequest = SKProductsRequest(productIdentifiers: [yearlySubscriptionProductID])
            productRequest.delegate = self
            productRequest.start()
        } else {
            showAlert( title: "Error", message: "In-App Purchases are disabled in your settings." )
        }
    }
    
    func productsRequest(_ request: SKProductsRequest, didReceive response: SKProductsResponse) {
        print("Found products count: \(response.products.count)")
        response.products.forEach { print("Found product: \($0.productIdentifier)") }
        
        guard let product = response.products.first else {
            print("Subscription product not found.")
            showAlert(title: "Error", message: "Subscription product not found.")
            return
        }
        yearlySubscriptionProduct = product
        print("Subscription product successfully loaded: \(product.productIdentifier)")
    }

    private func completeSubscriptionPurchase() {
        print("Completing subscription purchase...")
        isSubscribed = true
        updateUI()
        showAlert(title: "Message", message: "Thank you for subscribing!")
    }

    func paymentQueue(_ queue: SKPaymentQueue, updatedTransactions transactions: [SKPaymentTransaction]) {
        for transaction in transactions {
            switch transaction.transactionState {
            case .purchased, .restored:
                completeSubscriptionPurchase()
                SKPaymentQueue.default().finishTransaction(transaction)
            case .failed:
                if let error = transaction.error as? SKError, error.code != .paymentCancelled {
                    let errorMessage = "Transaction error: \(error.localizedDescription)"
                    if let presentedVC = presentedViewController as? SubscriptionViewController {
                        presentedVC.handleTransactionError(errorMessage)
                    } else {
                        showAlert(title: "Error", message: errorMessage)
                    }
                }
                SKPaymentQueue.default().finishTransaction(transaction)
            default:
                break
            }
        }
    }

    private func updateUI() {                      // Updates the UI based on subscription status
        DispatchQueue.main.async { [weak self] in
            guard let self = self else { return }
            guard let commentsTextView = self.commentsTextView else {     // Safely unwrapping commentsTextView
                print("commentsTextView is nil. Exiting updateUI early.")
                return
            }
            if let currentProgram = self.currentProgram {  // Assuming updateTextViewWithFormattedText is correctly handling optionals
                self.updateTextViewWithFormattedText(airportName:  currentProgram.airportName, locationOfTest: currentProgram.location, comments: currentProgram.comment)
            } else { commentsTextView.text = "" }
            commentsTextView.isScrollEnabled = true   // Now using safely unwrapped commentsTextView
            commentsTextView.isEditable = false
            commentsTextView.isSelectable = false
            commentsTextView.textContainerInset = UIEdgeInsets(top: 8, left: 4, bottom: 8, right: 4)
            let hasPrograms = self.programs.count > 0
            self.previousProgram.isEnabled = hasPrograms
            self.start_button.isEnabled = hasPrograms
            let buttonTitle = self.isSubscribed ? "Start" : "Subscribe"
            self.start_button.setTitle(buttonTitle, for: .normal)
            self.start_button.isEnabled = hasPrograms
            self.previousProgram.isEnabled = hasPrograms
            self.nextProgram.isEnabled = hasPrograms
            self.configure_button.isEnabled = hasPrograms
            self.review_button.isEnabled = hasPrograms
            self.delete_button.isEnabled = hasPrograms
        }
    }
    
    func removeProgram() {
        guard let currentProgram = currentProgram else {
            print("No program selected or available to delete."); return }
        programs.remove(at: current_program_index)    // Delete the program from the local array
        let fileName = "program_id_\(currentProgram.programId).json"   // Delete the program file from the document directory
        let documentDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first
        let fileURL = documentDirectory?.appendingPathComponent(fileName)
        do {
            if let fileURL = fileURL {
                try FileManager.default.removeItem(at: fileURL)
                print("Deleted program at \(fileURL)")
            }
        } catch {
            print("Error deleting program: \(error)")
        }
        if programs.isEmpty {  // Update the current_program_index and UI
            current_program_index = 0
            self.currentProgram = nil
        } else {
            if current_program_index >= programs.count {
                current_program_index = programs.count - 1 // Move to last
            }
            self.currentProgram = programs[current_program_index]
            updateUI() // Refresh the UI with the new current program
        }
    }
    
    func loadCurrentProgram() {
        programs = programDataSource.loadPrograms() // Load the programs
        DispatchQueue.main.async {  // Check if there are no programs and safely update the UI
            guard !self.programs.isEmpty else {
                // Safely update the UI elements
                self.commentsTextView?.text = "You do not have any programs. Use the New button to create the program."
                self.start_button?.isEnabled = false
                self.configure_button?.isEnabled = false
                self.review_button?.isEnabled = false
                self.delete_button?.isEnabled = false
                self.previousProgram?.isEnabled = false
                self.nextProgram?.isEnabled = false
                return
            }
            self.start_button?.isEnabled = true // There are programs, safely enable the UI elements
            self.configure_button?.isEnabled = true
            self.review_button?.isEnabled = true
            self.delete_button?.isEnabled = true
            self.previousProgram?.isEnabled = true
            self.nextProgram?.isEnabled = true
            if self.current_program_index < self.programs.count {               // Safely access the current
                self.currentProgram = self.programs[self.current_program_index] // program based on the
            }                                                                   // current index.
            self.start_button?.layer.borderColor = UIColor.black.cgColor
            self.start_button?.layer.borderWidth = 1
            self.start_button?.layer.cornerRadius = 3
            self.configure_button?.layer.borderColor = UIColor.black.cgColor
            self.configure_button?.layer.borderWidth = 1
            self.configure_button?.layer.cornerRadius = 3
            self.delete_button?.layer.borderColor = UIColor.black.cgColor
            self.delete_button?.layer.borderWidth = 1
            self.delete_button?.layer.cornerRadius = 3
            self.previousProgram?.layer.borderColor = UIColor.black.cgColor
            self.previousProgram?.layer.borderWidth = 1
            self.previousProgram?.layer.cornerRadius = 3
            self.nextProgram?.layer.borderColor = UIColor.black.cgColor
            self.nextProgram?.layer.borderWidth = 1
            self.nextProgram?.layer.cornerRadius = 3
            self.review_button?.layer.borderColor = UIColor.black.cgColor
            self.review_button?.layer.borderWidth = 1
            self.review_button?.layer.cornerRadius = 3
            self.new_button?.layer.borderColor = UIColor.black.cgColor
            self.new_button?.layer.borderWidth = 1
            self.new_button?.layer.cornerRadius = 3
            self.updateUI() // Update the rest of the UI
        }
    }
    
    private func presentSubscriptionViewController() {
        guard let product = yearlySubscriptionProduct else {
            showAlert(title: "Error", message: "Unable to load subscription product.")
            return
        }
        let subscriptionVC = SubscriptionViewController(subscriptionProduct: product)
        subscriptionVC.delegate = self  // Set delegate to handle errors
        subscriptionVC.modalPresentationStyle = .fullScreen
        present(subscriptionVC, animated: true, completion: nil)
    }

    private func showAlert(title: String = "Notice", message: String) {
        DispatchQueue.main.async { [weak self] in                       // Check if the view controller
            guard let self = self else { return }                       // is in the view hierarchy
            guard self.isViewLoaded && self.view.window != nil else {   // before presenting
                print("Unable to present alert because the view is not in the window hierarchy.")
                return
            }
            let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
            let okAction = UIAlertAction(title: "OK", style: .default, handler: nil)
            alertController.addAction(okAction)
            self.present(alertController, animated: true, completion: nil)
        }
    }
    
    @objc func saveButtonTapped() {
        guard let airportName = self.currentProgram?.airportName,
              let location = self.currentProgram?.location,
              let comment = self.currentProgram?.comment else {
            print("Error: One of the fields is empty")
            return }
        let uniqueID = UUID().uuidString
        // let newProgram = Program( programIdArg: uniqueID, airportName: airportName, location: location, comment: comment )
        // let programDataSource = ProgramDataSource()

    }
    
    @IBAction func startButtonTapped(_ sender: UIButton) {
        print( "start button tapped from UIButton." )}
    
    @IBAction func start_button_tapped(_ sender: Any) {
        if isSubscribed {
            print( "User has a valid subscription. Starting program..." )
        } else {
            guard let product = yearlySubscriptionProduct else {
                print("Unable to initiate subscription purchase as product is nil.")
                showAlert(title: "Error", message: "Unable to start subscription purchase.")
                return
            }
            print("Prompting user to subscribe...")
            // let payment = SKPayment(product: product)
            // SKPaymentQueue.default().add(payment)
            presentSubscriptionViewController()        }
    }
   
    
    override func viewDidLoad() {
        print( "ViewController viewDidLoad called" )
        super.viewDidLoad()
        
        version_text?.isEditable = false
        version_text?.isSelectable = false
        
        // Create the full text with copyright information and the link
        let fullText = "NAC-DFD Version 2.1\n© 2024\nNAC Dynamics, LLC.\n\nTerms and Conditions"
        let attributedString = NSMutableAttributedString(string: fullText)
        
        // Define the range of "Terms of use" and add the link attribute to it
        let termsRange = (fullText as NSString).range(of: "Terms and Conditions")
        attributedString.addAttribute(.link, value: "https://airportnac.com/privacy-policy/", range: termsRange)
        
        version_text?.attributedText = attributedString
        version_text?.textAlignment = .left
        version_text?.font = UIFont.systemFont(ofSize: 18)
        version_text?.linkTextAttributes = [
            .foregroundColor: UIColor.systemBlue,
            .underlineStyle: NSUnderlineStyle.single.rawValue
        ]

        SKPaymentQueue.default().add(self)  // Start observing the payment queue for subscription transactions
        fetchSubscriptionProduct()          // Fetch the subscription product info from App Store
        loadCurrentProgram()                // Update UI for programs and other initialization tasks
        updateUI()
        DispatchQueue.main.async {          // update the UI
            if let textView = self.commentsTextView {
                textView.layer.borderWidth = 1.0
                self.commentsTextView.layer.borderColor = UIColor.black.cgColor
            }
            self.view.backgroundColor = .white
            self.view.backgroundColor = UIColor.white
            self.loadCurrentProgram()
        }
    }
}

extension ViewController: AddProgramViewControllerDelegate {
    func didSaveProgram(_ controller: AddProgramViewController) {
        DispatchQueue.main.async { self.accelerationController?.sensorService.stop() }
        programs = programDataSource.loadPrograms()
        self.current_program_index = programs.count - 1 // Move to the last program in the list
        self.currentProgram = programs[ self.current_program_index ]
        DispatchQueue.main.async { [ weak self ] in
            controller.dismiss(animated: true ) { [weak self] in
                self?.navigationController?.popViewController(animated: true)
            }
        }
        updateUI()
    }
}

extension ViewController: SubscriptionViewControllerDelegate {ful
    func subscriptionViewControllerDidFailTransaction(_ controller: SubscriptionViewController, error: String) {
        controller.dismiss(animated: true) {
            self.showAlert(title: "Transaction Error", message: error)
        }
    }
}
```

When the "Subscribe" button is tapped, the subscription is handled, but the SubscriptionViewController is not dismissed.  Please fix this issue.
