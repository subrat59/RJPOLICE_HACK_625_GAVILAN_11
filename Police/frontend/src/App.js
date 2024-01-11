import logo from './logo.svg';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import Login from './Components/Login/Login';
import Dashboard from './Components/Dashboard/Dashboard';
import Card from './Components/Card/Card';
import Archieve from './Components/Archieve/Archieve';
import HistoryCard from './Components/History/History';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<Login/>}/>
        <Route path='/dashboard' element={<Dashboard/>}/>
        <Route path='/cards' element={<Card/>} />
        <Route path='/archieves' element={<Archieve/>} />
        <Route path='/history' element={<HistoryCard/>} />
      </Routes>
    </div>
  );
}

export default App;
