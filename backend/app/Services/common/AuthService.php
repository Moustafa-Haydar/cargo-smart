<?php

namespace App\Services\Common;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\LoginRequest;
use PHPOpenSourceSaver\JWTAuth\Facades\JWTAuth;

class AuthService
{

    public static function login(Request $request)
    {
        $credentials = $request->validated();

        $token = JWTAuth::attempt($credentials);

        if (!$token) {
            return null;
        }

        $user = JWTAuth::user();
        $user->token = $token;
        return $user;
    }


}
