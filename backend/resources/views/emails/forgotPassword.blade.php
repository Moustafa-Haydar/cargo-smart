{{-- resources/views/emails/forgot-password.blade.php --}}
<p>Hi {{ $user->name ?? $user->username }},</p>
<p>Click the link below to reset your password:</p>
<p><a href="{{ $url }}">{{ $url }}</a></p>
<p>This link expires in {{ config('auth.passwords.users.expire') }} minutes.</p>