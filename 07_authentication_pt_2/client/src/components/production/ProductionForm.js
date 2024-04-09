import React, {useState, useEffect} from 'react'
import styled from 'styled-components'
import { useNavigate, useOutletContext } from 'react-router-dom'

import { object, string, number, date, bool } from 'yup';
import { Formik } from 'formik';
import toast from "react-hot-toast"
// 7.✅ Use yup to create client side validations
let productionSchema = object({
  title: string()
    .min(2, "Titles must be at least 2 chars")
    .max(50, "Titles must be max 50 chars")
    .required("Title is required"),
  genre: string()
    .oneOf(["Drama", "Musical", "Opera"])
    .required("Genre is required"),
  budget: number()
    .positive("Budget has to be a positive number")
    .max(500000000, "Budget cannot be higher than 500000000")
    .required("Budget is required"),
  image: string()
    .test("is-url", "Images must be in the valid format (jpg, jpeg, png)", (value) => {
      const regexPattern = /^https?:\/\/.*\.(?:png|jpeg|jpg)$/g;
      return regexPattern.test(value)
    }),
  director: string()
    .min(2, "Directors must be at least 2 chars")
    .required("Director is required"),
  // description: string()
  //   .min(10, "Description must be at least 10 chars")
  //   .required("Description is required"),
  // ongoing: bool().required("Ongoing is required"), //! MISSING - DECIDE IF IT"S WORTH ADDING IT TO THE FORM
});


function ProductionForm() {
  const { addProduction, currentUser } = useOutletContext()
  const [backendError, setBackendError] = useState("");

  const navigate = useNavigate()

  useEffect(() => {
    if (!currentUser) {
      navigate("/registration")
      toast.error("Access Denied, login required!")
    } 
  }, [currentUser, navigate]);

  // 9.✅ useFormik hook

    return (
      <div className='App'>
        <div className="error-message">{backendError}</div>
        <Formik
          initialValues={{title: '', genre: '', budget: '', description: '', director: '', image: ''}}
          validationSchema={productionSchema}
          onSubmit={(values) => {
            fetch("/productions", {
              method: "POST",
              headers: {
                "Content-Type": "application/json"
              },
              body: JSON.stringify({ ...values, ongoing: true})
            })
            .then(resp => {
              if (resp.status === 201) {
                resp.json().then(createdProduction => {
                  addProduction(createdProduction)
                  return createdProduction
                }).then(createdProduction => navigate(`/productions/${createdProduction.id}`))
              } else {
                return resp.json().then(errorObj => {
                  let finalError = ""
                  debugger
                  for (let key in errorObj.message) {
                    finalError += errorObj.message[key]
                  }
                  setBackendError(finalError)
                })
              }
            })
            .catch(setBackendError)
          }}
        >
          {({
            values,
            errors,
            touched,
            handleChange,
            handleBlur,
            handleSubmit,
            isSubmitting,
          }) => (
            <Form onSubmit={handleSubmit}>
              <label>Title </label>
              <input type='text' name='title' onChange={handleChange} onBlur={handleBlur} value={values.title}/>
              {errors.title && touched.title && <div className='error-message show'>{errors.title}</div>}

              <label> Genre</label>
              <input type='text' name='genre' onChange={handleChange} onBlur={handleBlur} value={values.genre}/>
              {errors.genre && touched.genre && <div className='error-message show'>{errors.genre}</div>}

              <label>Budget</label>
              <input type='number' name='budget' onChange={handleChange} onBlur={handleBlur} value={values.budget}/>
              {errors.budget && touched.budget && <div className='error-message show'>{errors.budget}</div>}

              <label>Image</label>
              <input type='text' name='image'  onChange={handleChange} onBlur={handleBlur} value={values.image}/>
              {errors.image && touched.image && <div className='error-message show'>{errors.image}</div>}

              <label>Director</label>
              <input type='text' name='director'onChange={handleChange} onBlur={handleBlur} value={values.director}/>
              {errors.director && touched.director && <div className='error-message show'>{errors.director}</div>}

              <label>Description</label>
              <textarea type='text' rows='4' cols='50' name='description' onChange={handleChange} onBlur={handleBlur} value={values.description}/>
              {errors.description && touched.description && <div className='error-message show'>{errors.description}</div>}

              <input type='submit' disabled={isSubmitting} />
            </Form>
          )}
        </Formik> 
      </div>
    )
  }
  
  export default ProductionForm

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