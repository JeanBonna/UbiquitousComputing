package controller

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"GolangApi/database"
	"GolangApi/models"
)

// GetUsers: lista usuarios
func GetUsers(c *gin.Context) {
	query := `SELECT id, name, email, username, password, created_at, updated_at FROM users ORDER BY id`
	rows, err := database.DB.Query(query)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Erro ao buscar usuários"})
		return
	}
	defer rows.Close()

	var users []models.User
	for rows.Next() {
		var user models.User
		err := rows.Scan(
			&user.ID,
			&user.Name,
			&user.Email,
			&user.Username,
			&user.Password,
			&user.CreatedAt,
			&user.UpdatedAt,
		)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Erro ao processar usuários"})
			return
		}
		users = append(users, user)
	}

	c.JSON(http.StatusOK, users)
}

// GetUserByID - busca usuario por id
func GetUserByID(c *gin.Context) {
	id := c.Param("id")
	query := `SELECT id, name, email, username, password, created_at, updated_at FROM users WHERE id = $1`

	var user models.User
	err := database.DB.QueryRow(query, id).Scan(
		&user.ID,
		&user.Name,
		&user.Email,
		&user.Username,
		&user.Password,
		&user.CreatedAt,
		&user.UpdatedAt,
	)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuário não encontrado"})
		return
	}

	c.JSON(http.StatusOK, user)
}


// CreateUser - cria um usuário
func CreateUser(c *gin.Context) {
	var user models.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	query := `INSERT INTO users (name, email, username, password) VALUES ($1, $2, $3, $4) RETURNING id`
	err := database.DB.QueryRow(query, user.Name, user.Email, user.Username, user.Password).Scan(&user.ID)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Erro ao criar usuário"})
		return
	}

	c.JSON(http.StatusCreated, user)
}

// UpdateUser - atualiza um usuario
func UpdateUser(c *gin.Context) {
	id := c.Param("id")
	var user models.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	query := `UPDATE users SET name = $1, email = $2, username = $3 WHERE id = $4`
	result, err := database.DB.Exec(query, user.Name, user.Email, user.Username, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Erro ao atualizar usuário"})
		return
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuário não encontrado"})
		return
	}

	userID, _ := strconv.Atoi(id)
	user.ID = userID
	c.JSON(http.StatusOK, user)
}

// DeleteUser - deleta um usuário
func DeleteUser(c *gin.Context) {
	id := c.Param("id")
	query := `DELETE FROM users WHERE id = $1`

	result, err := database.DB.Exec(query, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Erro ao deletar usuário"})
		return
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		c.JSON(http.StatusNotFound, gin.H{"error": "Usuário não encontrado"})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}