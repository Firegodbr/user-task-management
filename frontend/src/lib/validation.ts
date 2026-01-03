import { toast } from "react-toastify";
import api from "./api";
export const validateRegistration = async (
  username: string,
  pw1: string,
  pw2: string
): Promise<boolean> => {
  // Check sizes
  if (username.length < 5 || pw1.length < 8 || pw2.length < 8) {
    toast.error("Username or Password is too short.");
    console.error("Username or Password is too short.");
    return false;
  }

  // Check if password has special chars and a number
  if (!/^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/.test(pw1)) {
    toast.error(
      "Password must contain at least one number and one special character."
    );
    console.error(
      "Password must contain at least one number and one special character."
    );
    return false;
  }

  // Check passwords are the same
  if (pw1 !== pw2) {
    toast.error("The passwords do not match.");
    console.error("The passwords do not match.");
    return false;
  }

  // Check username format: Only alphanumeric characters and underscores
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    toast.error("Username can only contain letters, numbers, and underscores.");
    console.error(
      "Username can only contain letters, numbers, and underscores."
    );
    return false;
  }

  // Check if password contains uppercase and lowercase letters
  if (!/[A-Z]/.test(pw1) || !/[a-z]/.test(pw1)) {
    toast.error("Password must contain both uppercase and lowercase letters.");
    console.error(
      "Password must contain both uppercase and lowercase letters."
    );
    return false;
  }
  if (await isUsernameTaken(username)) {
    toast.error("Username is already taken.");
    console.error("Username is already taken.");
    return false;
  }

  return true;
};

const isUsernameTaken = async (username: string): Promise<boolean> => {
  try {
    const response = await api.get("/auth/check-user-exists", {
      params: { username },
    });
    if (response.status === 200) {
      const data = response.data;
      toast.success(data.message);
      return Boolean(data.message);
    } else throw Error("Registration check failed");
  } catch (error: unknown) {
    if (error instanceof Error) toast.error(error.message);
    console.error(error);
    return true;
  }
};
