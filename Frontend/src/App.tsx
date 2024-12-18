import Cryption from './components/cryptionBox'
import Background from './components/background'
function App() {

  return (
    <>
      <Background />
      <Cryption operation = "Encryption"/>
      <Cryption operation = "Decryption"/>
    </>
  )
}

export default App
