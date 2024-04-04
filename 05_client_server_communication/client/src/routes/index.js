import { createBrowserRouter } from 'react-router-dom'
import App from '../App'
import Home from '../components/pages/Home'
import Error from '../components/errors/Error'
import ProductionForm from '../components/production/ProductionForm'
import ProductionDetail from '../components/production/ProductionDetail'
import ProductionEdit from '../components/production/ProductionEdit'

export const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        errorElement: <Error />,
        children: [
            {
                path: "/",
                index: true,
                element: <Home />
            },
            {
                path: "productions/new",
                element: <ProductionForm />
            },
            {
                path: "productions/:productionId/edit",
                element: <ProductionEdit />
            },
            {
                path: "/productions/:productionId",
                element: <ProductionDetail />
            }
        ]
    }
])