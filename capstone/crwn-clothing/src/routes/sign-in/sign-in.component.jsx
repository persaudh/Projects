import { useEffect } from "react";
import { getRedirectResult } from "firebase/auth";
import Button from "../../components/button/button.component";

import {
  auth,
  signInWithGooglePopup,
  signInWithGoogleRedirect,
  createUserDocumentFromAuth,
} from "../../utils/firebase/firebase.utils";

import SignUpForm from "../../components/sign-up-form/sign-up-form.component";

const SignIn = () => {
  const usePopup = true;

  const logGoogleUser = async () => {
    const { user } = await signInWithGooglePopup();
    if (user) {
      const userDocRef = await createUserDocumentFromAuth(user);
    }
  };

  // This effect runs when the component mounts to check for a redirect result
  useEffect(() => {
    const response = async () => await getRedirectResult(auth);
    if (response) {
      const userDocRef = async () =>
        await createUserDocumentFromAuth(response.user);
    }
  }, []);
  const logGoogleUserRedirect = async () => {
    const { user } = await signInWithGoogleRedirect();
    if (user) {
      const userDocRef = await createUserDocumentFromAuth(user);
    }
  };

  return (
    <div>
      <h1>Sign In Page</h1>
      <p>Please sign in to continue.</p>
      {usePopup ? (
        <Button onClick={logGoogleUser} buttonType="google">Sign in</Button>
      ) : (
        <Button onClick={logGoogleUserRedirect} buttonType="google">
          Sign in with Google redirect
        </Button>
      )}
      <SignUpForm />
    </div>
  );
};
export default SignIn;
