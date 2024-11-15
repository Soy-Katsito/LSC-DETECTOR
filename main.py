import org.opencv.core.*;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;
import org.opencv.highgui.HighGui;
import com.google.mediapipe.solutions.hands.Hands;
import com.google.mediapipe.solutions.facemesh.FaceMesh;
import com.google.mediapipe.solutions.drawing_utils.DrawingUtils;
import com.google.mediapipe.solutions.drawing_styles.DrawingStyles;

public class HandDetection {
    static {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
    }

    private static Hands handsDetector;
    private static FaceMesh faceMeshDetector;
    private static DrawingUtils drawingUtils;
    private static DrawingStyles drawingStyles;

    public static void main(String[] args) {
        try {
            Core.getVersionString();
        } catch (UnsatisfiedLinkError e) {
            System.out.println("Como xuxa quieres que funcione si no tienes ni la librería instalada!!, era mejor que no nacieras :v");
            System.exit(1);
        }

        try {
            Class.forName("com.google.mediapipe.solutions.hands.Hands");
        } catch (ClassNotFoundException e) {
            System.out.println("Instálate el mediapipe, npc!!!!1!!1!!");
            System.exit(1);
        }

        handsDetector = new Hands(Hands.createSolutionOptions()
                .setStaticImageMode(false)
                .setMaxNumHands(2)
                .setMinDetectionConfidence(0.7f)
                .setMinTrackingConfidence(0.7f));

        faceMeshDetector = new FaceMesh(FaceMesh.createSolutionOptions().setMaxNumFaces(1));
        drawingUtils = new DrawingUtils();
        drawingStyles = new DrawingStyles();

        VideoCapture cap = new VideoCapture(0);
        if (!cap.isOpened()) {
            System.out.println("Huh? La cámara no abrió, toca explotar");
            System.exit(1);
        }

        cap.set(Videoio.CAP_PROP_FRAME_WIDTH, 640);
        cap.set(Videoio.CAP_PROP_FRAME_HEIGHT, 480);

        Mat frame = new Mat();
        while (true) {
            if (!cap.read(frame)) {
                System.out.println("La cámara no se lee, down!!!! arregla eso, npc.");
                break;
            }

            Imgproc.GaussianBlur(frame, frame, new Size(5, 5), 0);
            Mat rgbFrame = new Mat();
            Imgproc.cvtColor(frame, rgbFrame, Imgproc.COLOR_BGR2RGB);

            Hands.Result resultsHands = handsDetector.process(rgbFrame);
            FaceMesh.Result resultsFaceMesh = faceMeshDetector.process(rgbFrame);

            boolean letraDetectada = false;

            if (resultsHands.multiHandLandmarks() != null) {
                for (NormalizedLandmarkList handLandmarks : resultsHands.multiHandLandmarks()) {
                    drawingUtils.drawLandmarks(frame, handLandmarks, Hands.HAND_CONNECTIONS);
                }

                if (detectLetterA(resultsHands.multiHandLandmarks())) {
                    Imgproc.putText(frame, "A", new Point(50, 50), Imgproc.FONT_HERSHEY_SIMPLEX, 1, new Scalar(108, 84, 227), 2);
                    System.out.println("Veo la letra (A) :0, yipee!");
                    letraDetectada = true;
                }

                if (detectLetterB(resultsHands.multiHandLandmarks())) {
                    Imgproc.putText(frame, "B", new Point(50, 50), Imgproc.FONT_HERSHEY_SIMPLEX, 1, new Scalar(108, 84, 227), 2);
                    System.out.println("Veo la letra (B) :0, yipee!");
                    letraDetectada = true;
                }

                if (detectLetterC(resultsHands.multiHandLandmarks())) {
                    Imgproc.putText(frame, "C", new Point(50, 50), Imgproc.FONT_HERSHEY_SIMPLEX, 1, new Scalar(108, 84, 227), 2);
                    System.out.println("Veo la letra (C) :0, yipee!");
                    letraDetectada = true;
                }
            }

            if (resultsFaceMesh.multiFaceLandmarks() != null) {
                for (NormalizedLandmarkList faceLandmarks : resultsFaceMesh.multiFaceLandmarks()) {
                    drawMouthMesh(frame, faceLandmarks);
                }
            }

            if (!letraDetectada) {
                System.out.println("No veo una letra, npc");
            }

            HighGui.imshow("cepe", frame);
            if (HighGui.waitKey(1) == 'q') {
                break;
            }
        }

        cap.release();
        HighGui.destroyAllWindows();
    }

    private static void drawMouthMesh(Mat image, NormalizedLandmarkList faceMesh) {
        drawingUtils.drawLandmarks(
            image,
            faceMesh,
            FaceMesh.FACEMESH_LIPS,
            null,
            drawingStyles.getDefaultFaceMeshContoursStyle());
    }

    private static boolean detectLetterA(List<NormalizedLandmarkList> hands) {
        for (NormalizedLandmarkList hand : hands) {
            NormalizedLandmark[] landmarks = hand.getLandmarkList().toArray(new NormalizedLandmark[0]);
            if (landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.THUMB_IP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.INDEX_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.MIDDLE_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.RING_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.PINKY_PIP.ordinal()].getY()) {
                return true;
            }
        }
        return false;
    }

    private static boolean detectLetterB(List<NormalizedLandmarkList> hands) {
        for (NormalizedLandmarkList hand : hands) {
            NormalizedLandmark[] landmarks = hand.getLandmarkList().toArray(new NormalizedLandmark[0]);
            if (landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getX() < landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.INDEX_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.MIDDLE_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.RING_FINGER_PIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.PINKY_PIP.ordinal()].getY() &&
                Math.abs(landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getX() - landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getX()) < 0.05 &&
                Math.abs(landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getX() - landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getX()) < 0.05 &&
                Math.abs(landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getX() - landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getX()) < 0.05) {
                return true;
            }
        }
        return false;
    }

    private static boolean detectLetterC(List<NormalizedLandmarkList> hands) {
        for (NormalizedLandmarkList hand : hands) {
            NormalizedLandmark[] landmarks = hand.getLandmarkList().toArray(new NormalizedLandmark[0]);
            if (landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getX() > landmarks[Hands.HandLandmark.THUMB_IP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getX() > landmarks[Hands.HandLandmark.INDEX_FINGER_PIP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getX() > landmarks[Hands.HandLandmark.MIDDLE_FINGER_PIP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getX() > landmarks[Hands.HandLandmark.RING_FINGER_PIP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getX() > landmarks[Hands.HandLandmark.PINKY_PIP.ordinal()].getX() &&
                landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.INDEX_FINGER_TIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.MIDDLE_FINGER_TIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.THUMB_TIP.ordinal()].getY() > landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getY() &&
                landmarks[Hands.HandLandmark.PINKY_TIP.ordinal()].getY() < landmarks[Hands.HandLandmark.RING_FINGER_TIP.ordinal()].getY()) {
                return true;
            }
        }
        return false;
    }
}

