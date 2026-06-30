import { useState, useRef, useEffect } from "react";


import Header from "./components/Header";
import CameraFeed from "./components/CameraFeed";
import TranslationCard from "./components/TranslationCard";
import ConfidenceBar from "./components/ConfidenceBar";
import Controls from "./components/Controls";
import HistoryPanel from "./components/HistoryPanel";
import StatusPanel from "./components/StatusPanel";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:5001";

function App() {

  useEffect(() => {
  return () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };
}, []);

  const intervalRef = useRef(null);
  const webcamRef = useRef(null);
  
  const [translation, setTranslation] = useState(
    "Press Start to begin translation"
  );

  const [cameraOn, setCameraOn] = useState(true);

  const [confidence, setConfidence] = useState(92);

  const [history, setHistory] = useState([]);

  const [isProcessing, setIsProcessing] = useState(false);

  const handleStart = () => {
    if (intervalRef.current) return;

    setIsProcessing(true);
    setTranslation("Processing...");

    intervalRef.current = setInterval(async () => {
      if (!webcamRef.current) return;

      const imageSrc = webcamRef.current.getScreenshot();
      if (!imageSrc) return;

      try {
        const response = await fetch(
          `${BACKEND_URL}/predict`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: imageSrc })
          }
        );

        const data = await response.json();

        if (data.translation) {
          setTranslation(data.translation);

          setConfidence(
            Math.round(data.confidence * 100)
          );

          setHistory(prev => {
            if (prev[0] === data.translation)
              return prev;

            return [
              data.translation,
              ...prev
            ];
          });
        }
      } catch (error) {
        console.error(error);
        setTranslation("Backend Error");
      }
    }, 300);
  };

  const handleStop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    setIsProcessing(false);
    setTranslation("Translation Stopped");
  };

  const handleSpeak = () => {
    const speech =
      new SpeechSynthesisUtterance(translation);

    speechSynthesis.speak(speech);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Header />

      <main className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-6 p-6">
        <CameraFeed
          cameraOn={cameraOn}
          setCameraOn={setCameraOn}
          webcamRef={webcamRef}
        />

        <div className="space-y-4">
          <TranslationCard text={translation} />

          <StatusPanel
            cameraOn={cameraOn}
            translation={translation}
            isProcessing={isProcessing}
          />

          <ConfidenceBar confidence={confidence} />

          <Controls
            onStart={handleStart}
            onStop={handleStop}
            onSpeak={handleSpeak}
          />

          <HistoryPanel history={history} />
        </div>
      </main>
    </div>
  );
}

export default App;