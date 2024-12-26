import Cryption from './components/cryptionBox'
import Background from './components/background'
function App() {

  return (
    <>
      <Background />
      <h1 className="text-center text-6xl font-bold text-green-400 mb-4 pt-16">
      AES ENCRYPTION & DECRYTION
      </h1>
      <Cryption operation = "Encryption"/>
      <Cryption operation = "Decryption"/>
    </>
  )
}

export default App
