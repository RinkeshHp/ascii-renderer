import cv2 as cv
from curses import wrapper


CHAR_DENSITY_MAPPING = "@QB#NgWM8RDHdOKq9$6khEPXwmeZaoS2yjufF]}{tx1zv7lciL/\\|?*>r^;:_\"~,'.-`"
CHAR_DENSITY_MAPPING = CHAR_DENSITY_MAPPING[::-1]



def maprange(a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def main(stdscr):
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    termrows, termcols = stdscr.getmaxyx() # get the size of the terminal
    # print(termrows,termcols)
    rows = 0
    cols = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()


        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv.resize(frame, (termcols-1, termrows-1))
        # Our operations on the frame come here
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        # Display the resulting frame
        rows, cols = gray.shape
        # gray = cv.Canny(gray, 100,100)
        cv.imshow('Source', gray)
        stdscr.clear()
        frame_string = ""
        for i in range(rows):
            
            for j in range(cols):
                frame_string = frame_string +CHAR_DENSITY_MAPPING[int(maprange((0,255), (0,len(CHAR_DENSITY_MAPPING)-1), gray[i, j]))]
                # stdscr.addch(int(maprange((0,rows-1),(0,termrows-2),i)),int(maprange((0,cols-1),(0,termcols-2),j)) , CHAR_DENSITY_MAPPING[int(maprange((0,255), (0,len(CHAR_DENSITY_MAPPING)-1), gray[i, j]))])
                # stdscr.addch(i,j,CHAR_DENSITY_MAPPING[int(maprange((0,255), (0,len(CHAR_DENSITY_MAPPING)-1), gray[i, j]))])
            frame_string = frame_string + "\n"
        stdscr.addstr(0,0,frame_string)
        stdscr.refresh()
        print(frame_string)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    stdscr.getch()

wrapper(main)