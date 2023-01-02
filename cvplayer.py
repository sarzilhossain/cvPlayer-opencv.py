import cv2, platform, time, os

begin = False
SUPPORTED_FORMATS = ["mp4"]
VIDEO_RESOLUTION = (1280, 720)
manual = """Video Window controls:
'a' - seek backward
'd' - seek forward
'space' - pause
'Esc' - quit
"""


def show_help():

    open_help = "\nrun 'open PATH' to open an image or video file"
    if platform.system() == "Linux" or platform.system() == "Darwin":
        open_example = "example: 'open /home/username/Videos/file.mp4'"
    elif platform.system() == "Windows":
        open_example = "example: 'open C:\\\\Users\\\\username\\\\Videos\\\\video.mp4'"

    print("\n\nCommands: open, set resolution, exit/quit")
    print(
        open_help
        + "\nSupported Formats: {}".format(SUPPORTED_FORMATS)
        + "\n"
        + open_example
        + "\n"
    )
    print(
        "run 'set resolution WIDTHxHEIGHT' to change the resolution of video.\nBy default, it's set to 1280x720.\nexample: 'set resolution 1368x768'\n"
    )
    print(manual)
    main()


def open_media(command):

    global filepath
    command = command.split(" ")
    command.remove("open")
    filepath = " ".join(command)

    if len(filepath) == 0:
        print(
            "\nFILEPATH NOT SPECIFIED.\nPlease re-run 'open' by specifying en existing file path."
        )
    elif not os.path.exists(filepath):
        print(
            "\nFILEPATH DOESN'T EXIST.\nPlease re-run 'open' with an existing file path."
        )
    else:
        fileformat = filepath.split(".")[-1]
        print(fileformat)

        if fileformat in SUPPORTED_FORMATS:
            cvfuncstart(filepath)
        else:
            print(
                f"\nFORMAT NOT SUPPORTED.\nPlease re-run 'open' with a file the format of which is supported.\nSupported formats{SUPPORTED_FORMATS}"
            )
    main()


def set_resolution(command):
    global VIDEO_RESOLUTION

    try:
        x = command.split(" ")[-1]
        height = int(x.split("x")[0])
        width = int(x.split("x")[1])

        if height > 7680:
            print(
                "\nMAXIMUM RESOLUTION HEIGHT LIMIT SURPASSED\nPlease re-run 'set resolution' with the correct values"
            )
            return
        if width > 4320:
            print(
                "\nMAXIMUM RESOLUTION WIDTH LIMIT SURPASSED\nPlease re-run 'set resolution' with the correct values"
            )
            return

        VIDEO_RESOLUTION = (height, width)
        print("Resolution set to: {}".format(VIDEO_RESOLUTION))

    except Exception:
        print(
            "\nUNDEFINED INPUT. Please try again.\nexample: 'set resolution 1368x768'"
        )

    main()


def main():

    global begin, fileformat, SUPPORTED_FORMATS, VIDEO_RESOLUTION
    if begin == False:
        print("\ntype 'help' to show the help menu\n")
        print(manual)
        begin = True

    command = input("\n|cvplayer run| ").strip()

    if command == ("help"):
        show_help()
    elif command.startswith("open"):
        open_media(command)
    elif command == "quit" or command == "exit":
        exit()
    elif command.startswith("set"):
        if command.startswith("set resolution"):
            set_resolution(command)
    else:
        print("\nCOMMAND NOT RECOGNIZED.\nRun 'help' to see the commands.")
        main()


def reshape_img(frame, resolution):
    return cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)


def cvfuncstart(filepath):

    frames = 24
    SEEK_SECONDS = 10
    cap = cv2.VideoCapture(filepath)
    isPaused = False
    while cap.isOpened():
        try:
            time.sleep(1 / frames)

            if not isPaused:
                ret, frame = cap.read()

            frame = reshape_img(frame, VIDEO_RESOLUTION)
            cv2.imshow(filepath, frame)
            x = cv2.waitKeyEx(1)

            if x == ord("a"):
                cframe = cap.get(cv2.CAP_PROP_POS_FRAMES)
                cap.set(cv2.CAP_PROP_POS_FRAMES, cframe - frames * SEEK_SECONDS)
            elif x == ord("d"):
                cframe = cap.get(cv2.CAP_PROP_POS_FRAMES)
                cap.set(cv2.CAP_PROP_POS_FRAMES, cframe + frames * SEEK_SECONDS)
            elif x == 32:
                if isPaused == False:
                    isPaused = True
                else:
                    isPaused = False
            elif x == 27:
                break
        except cv2.error:
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
