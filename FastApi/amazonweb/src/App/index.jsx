// Entry point

import AppProvider from "./Provider"
import AppRoutes from "./Routes"

function App(){

    return (
        <AppProvider>
            <AppRoutes>

            </AppRoutes>
        </AppProvider>
    )
}

export default App;