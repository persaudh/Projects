import Directory from "../../components/directory/directory.component";
import categories from "../../categories.json";
import {Outlet} from "react-router-dom";

function Home() {
  return (
    <>
      <Directory categories={categories} />
      <Outlet />
    </>
  );
}

export default Home;
