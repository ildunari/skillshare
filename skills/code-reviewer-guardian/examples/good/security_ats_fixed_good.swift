
/* Info.plist fragment */
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <false/>
</dict>

import CryptoKit
func sha256(_ s: String) -> String {
    let digest = SHA256.hash(data: s.data(using: .utf8)!)
    return digest.map { String(format: "%02x", $0) }.joined()
}
