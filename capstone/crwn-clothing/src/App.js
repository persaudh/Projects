import "./App.css";
import Directory from "./components/directory/directory.component";
import categories from "./categories.json";

function App() {
  return (
    <Directory categories={categories}/>
  );
}

export default App;
