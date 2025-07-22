import { Outlet, Link  } from "react-router-dom";
import { Fragment } from "react";
import { ReactComponent as CrownLogo } from "../../assets/crown.svg";
import "./navagation.styles.scss";

const Navagation = () => {
  return (
    <Fragment>
      <div className="navigation"> 
        <Link className="nav-link" to="/">
          <CrownLogo className="logo-container" />
        </Link>
        <div className="nav-links-container">
          <Link className="nav-link" to="/shop">SHOP</Link>
          <Link className="nav-link" to="/auth">SIGN IN</Link>
        </div>
      </div>
      <Outlet />
    </Fragment>
  );
}

export default Navagation;