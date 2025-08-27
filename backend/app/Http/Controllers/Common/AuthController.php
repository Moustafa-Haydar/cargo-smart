<?php
namespace App\Http\Controllers\Common;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\common\AuthService;
use App\Http\Requests\LoginRequest;
use App\Traits\ResponseTrait;
use App\Models\User;
use Illuminate\Support\Str;
use Illuminate\Auth\Events\PasswordReset;


use Illuminate\Support\Facades\Password;
use Illuminate\Support\Facades\Hash;


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

    public function resetPasswordForm()
    {
        // display form to enter email for password reset
        // this will be frontend route
    }

    public function sendResetLink(Request $request)
    {
        $request->validate([
            'username' => 'required|string',
        ]);

        $status = AuthService::sendResetLink($request->input('username'));

        if ($status === true) {
            return $this->responseJSON(null, "Password reset link sent to your email.");
        } else {
            return $this->responseJSON(null, "Failed to send reset link.", 500);
        }
    }

    public function updatePasswordForm($token)
    {
        // display form to enter new password
        // this will be frontend route
    }

    public function updatePassword(Request $request)
    {
        // http://localhost:3000/reset-password?token=5426f392bd7be858963f8e8b5c95348b149023af217f38775dc936f4618d8e1e&email=moustafahaydar.eng%40gmail.com

        $request->validate([
            'username' => 'required|string',
            'password' => 'required|string|min:8|confirmed',
            'token' => 'required|string',
        ]);

        $user = User::where('username', $request->username)->first();
        if (!$user) {
            return $this->responseJSON(null, "User not found.", 404);
        }

        Log::info("Token: " . $request->token);

        $status = Password::reset(
            [
                'email' => $user->email,
                'token' => $request->token,
                'password' => $request->password,
                'password_confirmation' => $request->password_confirmation,
            ],

            function ($user) use ($request) {
                $user->forceFill([
                    'password' => Hash::make($request->password),
                ])->setRememberToken(Str::random(60));

                $user->save();
                event(new PasswordReset($user));
            }
        );

        Log::info("Password reset status: " . $status);
        // $status = AuthService::updatePassword($request);

        return $status === Password::PASSWORD_RESET
            ? $this->responseJSON(null, "Password has been reset successfully.")
            : $this->responseJSON(null, "Failed to reset password.", 500);

    }




}
