import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from "react-router-dom";
import TranslatorApp from "./TranslatorApp";
import SignInPage from "./SignInPage";


const App = () => {

  return (
    <Router>
      <Link to='/signin'>Sign In</Link>
        <br/>
        <Link to='/'>Home</Link>

      <Routes>
      <Route path='/' element={<TranslatorApp/>} />
      <Route path='/signin' element={<SignInPage/>} />
    
      </Routes>
      </Router>
  );
};

export default App;
