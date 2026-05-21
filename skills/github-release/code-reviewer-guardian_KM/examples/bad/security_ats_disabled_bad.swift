
/* Info.plist fragment */
<key>NSAppTransportSecurity</key>
<dict>
  <key>NSAllowsArbitraryLoads</key>
  <true/>
</dict>

// In code
import CommonCrypto
func hash(_ s: String) -> String {
    // MD5 usage
    return "md5:" + s
}
