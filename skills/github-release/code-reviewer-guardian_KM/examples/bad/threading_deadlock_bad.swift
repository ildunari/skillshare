
func doWork() {
    DispatchQueue.main.sync {
        print("Never do this from main thread - deadlock risk")
    }
}
