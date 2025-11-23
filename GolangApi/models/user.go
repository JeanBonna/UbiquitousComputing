package models

type User struct {
	ID       int    `json:"id"`
	Name     string `json:"name" binding:"required"`
	Email    string `json:"email" binding:"required,email"`
	User     string `json:"user" binding:"required"`
	Password string `json:"password,omitempty" binding:"required"`
}
