import Webcam from "react-webcam";

function CameraFeed({ cameraOn, setCameraOn, webcamRef }) {
  return (
    <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
      <h2 className="text-2xl font-semibold text-gray-900 mb-4">
        Camera Feed
      </h2>

      <div className="flex gap-3 mb-4">
        <button
          onClick={() => setCameraOn(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Enable Camera
        </button>

        <button
          onClick={() => setCameraOn(false)}
          className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
        >
          Disable Camera
        </button>
      </div>

      <div className="overflow-hidden rounded-lg border border-gray-200">
        {cameraOn ? (
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="w-full h-96 object-cover"
          />
        ) : (
          <div className="w-full h-96 flex items-center justify-center bg-gray-100 text-gray-500">
            Camera Disabled
          </div>
        )}
      </div>
    </div>
  );
}

export default CameraFeed;