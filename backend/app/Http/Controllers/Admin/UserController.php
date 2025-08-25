<?php
namespace App\Http\Controllers\Admin;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\Admin\UserService;
use App\Http\Requests\StoreUserRequest;
use App\Traits\ResponseTrait;
use Illuminate\Support\Facades\Log;
use Psy\Readline\Hoa\EventListens;

class UserController extends Controller
{
    use ResponseTrait;

    public function addUser(StoreUserRequest $request)
    {
        $user = UserService::addUser($request);
        return $this->responseJSON($user);
    }

    public function getAllUsers($id = null)
    {
        $users = UserService::getAllUsers($id);
        return $this->responseJSON($users);
    }


}