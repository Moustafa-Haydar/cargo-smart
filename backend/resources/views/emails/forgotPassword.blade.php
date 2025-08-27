<!DOCTYPE html>
<html>

<body>
    <p>Hi {{ $user->first_name ?? $user->name }},</p>
    <p>Click the link below to reset your password:</p>
    <p><a href="{{ $url }}">{{ $url }}</a></p>
    <p>If you didn’t request this, you can ignore this email.</p>
</body>

</html>