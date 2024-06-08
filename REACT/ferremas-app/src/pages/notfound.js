import Header from "../components/Header"

export default function NotFound() {
    return (
        <>
            <Header/>
            <div className='container'>
                <div className='mb-3 mt3'>
                    <h1>Error 404: Page not found</h1>
                </div>
            </div>
        </>
    )
}