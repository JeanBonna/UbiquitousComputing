// package models

// type User struct {
// 	ID       int    `json:"id"`
// 	Name     string `json:"name" binding:"required"`
// 	Email    string `json:"email" binding:"required,email"`
// 	User     string `json:"user" binding:"required"`
// 	Password string `json:"password,omitempty" binding:"required"`
// }

package models

type User struct {
	ID       int    `json:"id" db:"id"`
	Name     string `json:"name" binding:"required" db:"name"`
	Email    string `json:"email" binding:"required,email" db:"email"`
	Username string `json:"username" binding:"required" db:"username"`
	Password string `json:"password,omitempty" binding:"required" db:"password"`
}