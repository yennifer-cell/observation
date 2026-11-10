// Entry point

import AppProvider from "./Provider"
import AppRoutes from "./Routes"
import { Toaster } from 'react-hot-toast';

function App(){

    return (
        <AppProvider>
            <AppRoutes/>
            <Toaster/>
        </AppProvider>
    )
}

export default App;