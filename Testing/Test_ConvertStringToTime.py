import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ConvertStringToTime import ConvertStringToTime

def RunTest(string, shouldFail):
    print("Attempting to convert string '" + string + "' to time")
    result = ConvertStringToTime(string)

    if (result.Error):
        if (shouldFail == False):
            print(f"FAILURE: Error when converting {string}: {result.Error}\n")
            return False
        else:
            print(f"SUCCESS: Should have failed when converting {string}\n")
            return True
    else:
        if (shouldFail):
            print(f"FAILURE: Should have failed when converting {string}\n")
            return False
        else:
            print(f"SUCCESS: Delta ({result.GetDeltaString()}), Time [{str(result.DateTime)}]\n")
            return True


#  Test #001: Convert "three pm"
RunTest("three pm", False)

#  Test #002: Convert "one am"
RunTest("one am", False)

#  Test #003: Convert "five pm"
RunTest("five pm", False)

#  Test #004: Convert "nine am"
RunTest("nine am", False)

#  Test #005: Convert "twelve am"
RunTest("twelve am", False)

#  Test #005: Convert "twelve pm"
RunTest("twelve pm", False)

#  Test #006: Convert "twelve thirty pm"
RunTest("twelve thirty pm", False)

#  Test #006: Convert "twelve thirty five pm"
RunTest("twelve thirty five pm", False)

#  Test #006: Convert "ten oh eight am"
RunTest("ten oh eight am", False)

#  Test #006: Convert "thirteen oh eight am" (should fail)
RunTest("thirteen oh eight am", True)

#  Test #006: Convert "negative one oh eight am" (should fail)
RunTest("negative one oh eight am", True)

#  Test #006: Convert "seven fifty am"
RunTest("seven fifty am", False)

#  Test #006: Convert "seven sixty pm" (should fail)
RunTest("seven sixty pm", True)