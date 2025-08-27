<?php
namespace App\Http\Controllers\Common;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\common\AuthService;
use App\Http\Requests\LoginRequest;
use App\Traits\ResponseTrait;
use App\Models\User;

use Illuminate\Support\Facades\Log;

class AuthController extends Controller
{
    use ResponseTrait;
    public function login(LoginRequest $request)
    {

        Log::info("test here: " . $request['username']);

        // $user = AuthService::login($request);

        $credentials = $request->validated();

        // Use session-based auth (cookie)
        if (!Auth::guard('web')->attempt($credentials, true)) {
            return $this->responseJSON(null, "Invalid credentials", 401);
        }

        $request->session()->regenerate(); // prevent session fixation

        $user = Auth::user();
        return $this->responseJSON($user, "Login successful");
    }

    public function logout(Request $request)
    {
        Auth::guard('web')->logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return $this->responseJSON(null, "Logged out successfully");
    }

    public function sendResetLink(Request $request)
    {
        $request->validate([
            'username' => 'required|string|exists:users,username',
        ]);

        $status = AuthService::sendResetLink($request->input('username'));

        if ($status === true) {
            return $this->responseJSON(null, "Password reset link sent to your email.");
        } else {
            return $this->responseJSON(null, "Failed to send reset link.", 500);
        }
    }





}
