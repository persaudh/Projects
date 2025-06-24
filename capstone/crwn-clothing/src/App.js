import "./App.css";
import Home from "./routes/home/home.component";
import { Routes, Route } from "react-router-dom";
import Navagation from "./routes/navagation/navagation.component";
import SignIn from "./routes/sign-in/sign-in.component";

const Shop = () => {
  return (
    <div>
      <h1>Store</h1>
      <p>Welcome to the store!</p>
    </div>
  );
}

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navagation />} >
        <Route index element={<Home />} />
        <Route path="shop" element={<Shop />} />
        <Route path="sign-in" element={<SignIn />} />
      </Route>
    </Routes>
  );
};
export default App;
