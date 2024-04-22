import { useState } from 'react'
import {Link} from 'react-router-dom'
import styled from 'styled-components'
import { GiHamburgerMenu } from 'react-icons/gi'

function Header({ handleEdit, currentUser, updateCurrentUser }) {
 const [menu, setMenu] = useState(false)

  const handleDelete = () => {
    fetch("/logout", {method: "DELETE"})
    .then(resp => {
      if (resp.status === 204) {
        updateCurrentUser(null)
      }
    })
    .catch(err => console.log(err))
  }
    return (
        <Nav> 
         <NavH1>Flatiron Theater Company</NavH1>
         <Menu>
           {!menu?
           <div onClick={() => setMenu(!menu)}>
             <GiHamburgerMenu size={30}/> 
           </div>:
           <ul>
             <li onClick={() => setMenu(!menu)}>x</li>
              {currentUser ? (
                <>
                  <li onClick={handleDelete}>Logout</li>
                  <li ><Link to='/productions/new'>New Production</Link></li>
                </>
              ) : (
                  <li ><Link to='/registration'>Register</Link></li>
              )}
            <li><Link to='/'> Home</Link></li>
           </ul>
           }
         </Menu>

        </Nav>
    )
}

export default Header


const NavH1 = styled.h1`
font-family: 'Splash', cursive;
`
const Nav = styled.div`
  display: flex;
  justify-content:space-between;
  
`;

const Menu = styled.div`
  display: flex;
  align-items: center;
  a{
    text-decoration: none;
    color:white;
    font-family:Arial;
  }
  a:hover{
    color:pink
  }
  ul{
    list-style:none;
  }
  
`;