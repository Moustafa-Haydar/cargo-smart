<?php
namespace App\Http\Controllers\Common;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\common\AuthService;
use App\Http\Requests\LoginRequest;
use App\Traits\ResponseTrait;

use Illuminate\Support\Facades\Log;

class AuthController extends Controller
{
    use ResponseTrait;
    public function login(LoginRequest $request)
    {

        Log::info("test here: " . $request['username']);

        $user = AuthService::login($request);

        if ($user)
            return $this->responseJSON($user);

        return $this->responseJSON(null, "error", 401);
    }

}
