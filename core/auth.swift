import LocalAuthentication
import Foundation

let context = LAContext()
var error: NSError?

// Group to wait for async completion
let semaphore = DispatchSemaphore(value: 0)

if context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error) {
    context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: "Access J.A.R.V.I.S. Shadow Protocol") { success, authenticationError in
        if success {
            print("SUCCESS")
            exit(0)
        } else {
            print("FAILED")
            exit(1)
        }
        semaphore.signal()
    }
    semaphore.wait()
} else {
    print("UNAVAILABLE")
    exit(0)
}
