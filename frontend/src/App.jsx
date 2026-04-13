import Chatbot from "@/components/Chatbot";
import logo from "@/assets/images/logo.svg";

function App() {
  return (
    <div className="min-h-screen w-full bg-black">
      <header
        className="
        sticky top-0 z-50 
        bg-gradient-to-b from-red-700 via-red-600 to-red-800
        border-b border-red-900 shadow-xl
        rounded-b-3xl
      "
      >
        <div className="w-full px-4 py-3 flex items-center">
          <img src={logo} className="w-32" alt="logo" />
          <div className="ml-auto flex items-center gap-3">
            <div className="ml-auto flex items-center">
              <div className="h-5 w-5 rounded-full bg-red-400 shadow-[0_0_10px_rgba(255,80,80,0.9)] animate-pulse flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-red-200"></div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex flex-col w-full max-w-3xl mx-auto px-4">
        <Chatbot />
      </div>
    </div>
  );
}

export default App;
