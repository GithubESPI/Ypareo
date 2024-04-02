import Footer from "./components/Footer"
import Navbar from "./components/Navbar"
import Upload from "./components/Upload"

const App = () => {
  return (
    <div className="flex h-screen flex-col">
     <Navbar />
     <main className="flex-1">
      <Upload />
     </main>
     <Footer />
    </div>
  )
}

export default App