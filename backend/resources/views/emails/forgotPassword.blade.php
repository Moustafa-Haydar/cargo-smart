<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>Password Reset</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f6f8fa;
            color: #333;
            padding: 40px;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: #ffffff;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .button {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }

        .footer {
            margin-top: 30px;
            font-size: 12px;
            color: #777;
        }
    </style>
</head>

<body>
    <div class="container">
        <h2>Hello {{ $user->first_name }},</h2>

        <p>You requested to reset your password. Click the button below to proceed:</p>

        <a href="{{ $url }}" class="button">Reset Your Password</a>

        <p>If the button doesn’t work, copy and paste this URL into your browser:</p>
        <p><a href="{{ $url }}">{{ $url }}</a></p>

        <div class="footer">
            <p>This email was sent by CargoSmart. If you didn’t request a password reset, you can safely ignore this
                message.</p>
        </div>
    </div>
</body>

</html>