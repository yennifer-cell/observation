//expose the provider

import { useContext } from "react";
import AppContext from "../Provider/AppContext";

const useApp = () => {
  const context = useContext(AppContext);

  return context;
};

export default useApp;

