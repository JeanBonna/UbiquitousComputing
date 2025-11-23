package models

import "time"

type User struct {
	ID        int       `json:"id" db:"id"`
	Name      string    `json:"name" binding:"required" db:"name"`
	Email     string    `json:"email" binding:"required,email" db:"email"`
	Username  string    `json:"username" binding:"required" db:"username"`
	Password  string    `json:"password" binding:"required" db:"password"`
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}
