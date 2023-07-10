require('dotenv').config();
const express = require('express');
const axios = require('axios');

const app = express();

const PORT = process.env.PORT || 5000;

const baseUrl = process.env.BASE_URL;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
        return res.status(200).json({
                message: 'Okay',
                status: 'success',
        });
});

// @Get Users
app.get('/users', async (req, res) => {
        try {
                const { status, data } = await axios.get(`${baseUrl}/users`);

                if (status === 200) {
                        return res.status(status).json({
                                code: status,
                                status: 'success',
                                data,
                        });
                } else if (status !== 200) {
                        return res.status(status).json({
                                code: status,
                                data: null,
                        });
                }
        } catch (error) {
                const code = error?.response?.status;

                return res.status(code).json({
                        code,
                        data: null,
                        error: error?.message,
                });
        }
});

app.post('/users', async (req, res) => {
        try {
                const { status, data } = await axios.post(`${baseUrl}/users`, {
                        ...req.body,
                });

                if (status === 201) {
                        return res.status(status).json({
                                code: status,
                                data,
                                status: 'success',
                        });
                } else if (status !== 201) {
                        return res.status(status).json({
                                code: status,
                                data: null,
                        });
                }
        } catch (error) {
                return res.status(error?.response?.status).json({
                        data: null,
                        error: error.message,
                        code: error?.response?.status,
                });
        }
});

app.listen(PORT, () => console.log(`App listening on port: ${PORT}`));
