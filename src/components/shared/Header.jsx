import React from 'react'
import logo from "/assets/img/header/logo.png"
// import { Button } from '../ui/button'
import MobileNav from './MobileNav'
import NavItems from './NavItems'

const Header = () => {
  return (
    <header className="w-full border-b">
        <div className="wrapper flex items-center justify-between">
            <a href="/" className="w-36">
                <img src={logo} width={128} height={38} alt="ESPI_LOGO" />
            </a>

            <nav className="md:flex-between hidden w-full max-w-xs">
                <NavItems />
            </nav>

            <div className="flex w-32 justify-end gap-3">
                
                <MobileNav />
                {/* <Button asChild className="rounded-full" size="lg">
                    <a href="/">User</a>
                </Button> */}
            </div>
        </div>
    </header>
  )
}

export default Header