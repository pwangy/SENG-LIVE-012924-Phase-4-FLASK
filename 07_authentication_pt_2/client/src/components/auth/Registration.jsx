import React, { useState } from 'react'
import styled from 'styled-components'
import { useNavigate, useOutletContext } from 'react-router-dom'
import toast from "react-hot-toast"
import { object, string, number, date, bool } from 'yup';
import { useFormik } from 'formik';

const signupSchema = object({
  username: string()
    .min(2, "Usernames must be at least 2 chars long")
    .max(20, "Usernames must be max 20 chars")
    .required("Username is required"),
  email: string().email().required("Email is required"),
  password: string()
    .min(8, "Passwords must be at least 8 chars long")
    .matches(
      /[a-zA-Z0-9]/,
      "Passwords can only contain latin numbers and letters"
    )
    .required("Password is required"),
});
const signinSchema = object({
  email: string().email().required("Email is required"),
  password: string()
    .min(8, "Passwords must be at least 8 chars long")
    .matches(
      /[a-zA-Z0-9]/,
      "Passwords can only contain latin numbers and letters"
    )
    .required("Password is required"),
});

const initialValues = {
    username: "",
    email: "",
    password: ""
}
const Registration = () => {
    const [isLogin, setIsLogin] = useState(false);
    const {updateCurrentUser} = useOutletContext()
    const navigate = useNavigate()
    const requestUrl = isLogin ? "/login" : "/signup"
    const formik = useFormik({
        initialValues,
        validationSchema: isLogin ? signinSchema : signupSchema,
        onSubmit: (formData) => {
            fetch(requestUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            })
            .then(resp => {
                if (resp.ok) {
                    resp.json()
                    .then(updateCurrentUser)
                    .then(() => navigate("/"))
                } else {
                    return resp
                    .json()
                    .then((errorObj) => toast.error(errorObj.message));
                }
            })
        }
    })

    return (
      <div>
        <h2>Please Log In or Signup!</h2>
        <h3>{isLogin ? "Not a member?" : "Already a member?"}</h3>
        <button onClick={() => setIsLogin((currentState) => !currentState)}>
          {isLogin ? "Register Now!" : "Login!"}
        </button>

        <Form onSubmit={formik.handleSubmit}>
          {!isLogin && (
            <>
                <label>Username </label>
                <input
                    type="text"
                    name="username"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    value={formik.values.username}
                />
                {formik.errors.username && formik.touched.username && (
                    <div className="error-message show">{formik.errors.username}</div>
                )}
            </>
            )}
          <label>Email </label>
          <input
            type="text"
            name="email"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.email}
          />
          {formik.errors.email && formik.touched.email && (
            <div className="error-message show">{formik.errors.email}</div>
          )}
          <label>Password </label>
          <input
            type="password"
            name="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.password}
          />
          {formik.errors.password && formik.touched.password && (
            <div className="error-message show">{formik.errors.password}</div>
          )}

        <input type="submit" value={isLogin ? "Login!" : "Signup!"} />
          
        </Form>
      </div>
    );
}

export default Registration

const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `