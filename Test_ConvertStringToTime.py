from ConvertStringToTime import ConvertStringToTime

def RunTest(string):
    print("Attempting to convert string '" + string + "' to time")
    result = ConvertStringToTime(string)
    if (result.Error):
        print(f"FAILURE: Error when converting {string}: {result.Error}\n")
        return False
    
    print(f"SUCCESS: Delta ({result.GetDeltaString()}), Time [{str(result.DateTime)}]\n")
    return True


#  Test #001: Convert "three pm"
RunTest("three pm")

#  Test #002: Convert "one am"
RunTest("one am")

#  Test #003: Convert "five pm"
RunTest("five pm")

#  Test #004: Convert "nine am"
RunTest("nine am")

#  Test #005: Convert "twelve am"
RunTest("twelve am")

#  Test #005: Convert "twelve pm"
RunTest("twelve pm")

#  Test #006: Convert "twelve thirty pm"
RunTest("twelve thirty pm")

#  Test #006: Convert "twelve thirty five pm"
RunTest("twelve thirty five pm")

#  Test #006: Convert "twelve thirty five pm"
RunTest("ten oh eight am")

#  Test #006: Convert "twelve thirty five pm"
RunTest("thirteen oh eight am")

#  Test #006: Convert "twelve thirty five pm"
RunTest("negative one oh eight am")

#  Test #006: Convert "twelve thirty five pm"
RunTest("seven fifty am")

#  Test #006: Convert "twelve thirty five pm"
RunTest("seven sixty pm")