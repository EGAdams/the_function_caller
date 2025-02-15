import UIKit
import CoreMotion

class ViewController: UIViewController {
    let motionManager = CMMotionManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Start accelerometer updates
        if motionManager.isAccelerometerAvailable {
            motionManager.accelerometerUpdateInterval = 1.0 / 10.0 // Update 10 times per second
            motionManager.startAccelerometerUpdates(to: OperationQueue.current!) { (data, error) in
                if let validData = data {
                    self.postAccelerometerData(validData: validData)
                }
            }
        }
    }
    
    func postAccelerometerData(validData: CMAccelerometerData) {
        let url = URL(string: "https://your-server-endpoint.com/api/accelerometer")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        // Format data as JSON
        let json: [String: Any] = [
            "x": validData.acceleration.x,
            "y": validData.acceleration.y,
            "z": validData.acceleration.z,
            "timestamp": Date().timeIntervalSince1970 // optional timestamp
        ]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: json, options: [])
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        } catch {
            print("Error converting data to JSON: \(error)")
            return
        }
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error sending data: \(error)")
                return
            }
            print("Data sent successfully!")
        }
        task.resume()
    }
}