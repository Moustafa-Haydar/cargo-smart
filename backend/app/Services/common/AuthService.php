<?php

namespace App\Services\Common;
use App\Models\User;
use App\Mail\ForgotPassword;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\LoginRequest;
use Illuminate\Support\Facades\Password;

class AuthService
{
    public static function sendResetLink($username)
    {
        $user = User::where('username', $username)->first();
        if (!$user) {
            Log::info(message: 'No user found with username: ' . $username);
            return false;
        }

        $token = Password::createToken($user);

        $url = config('app.frontend_url') . '/reset-password?token=' . $token . '&email=' . urlencode($user->email);

        Mail::to(users: $user->email)->send(new ForgotPassword($user, $url));

        // debug
        Log::info(message: 'Invoice email sent successfully');

        return true;
    }

    public static function updatePassword(Request $request)
    {
        // to be implemented
        return true;
    }


}
