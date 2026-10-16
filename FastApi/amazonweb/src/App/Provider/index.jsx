import {  useState } from "react";
import AppContext from "./AppContext";

function Provider({ children }){

const [member,setMember]=useState(null)
const [token,setToken]=useState(null)

return (<AppContext.Provider value={{
    member,
    setMember,
    token,
    setToken
    }}>
        {children}
    </AppContext.Provider>
);
}

export default Provider;