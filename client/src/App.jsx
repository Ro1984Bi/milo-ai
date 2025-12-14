import { Route, Routes } from 'react-router-dom'
import Login from './components/Login'
import Signup from './components/Signup'
import Home from './components/Home'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <>
      <div>

        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          } />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Signup />} />

        </Routes>

      </div>
    </>
  )
}

export default App